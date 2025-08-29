using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Security.Cryptography.X509Certificates;

namespace ForecastingSystemApi
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);

            var projectId = builder.Configuration["Firebase:ProjectId"]; // Takes Firebase project ID from configuration
            var authority = $"https://securetoken.google.com/{projectId}"; // Firebases Open ID Connect (OIDC) issuer for this project

            // Registers & configures services in the app's Dependency Injection (DI) container before the app starts

            builder.Services
                .AddAuthentication(JwtBearerDefaults.AuthenticationScheme) // Sets JWT Bearer as default auth scheme
                .AddJwtBearer(options =>
                {
                    options.Authority = authority; // Token issuer (Firebase)
                    options.TokenValidationParameters = new TokenValidationParameters
                    {
                        ValidateIssuer = true, // Firebase is the only valid issuer of tokens
                        ValidIssuer = authority,
                        ValidateAudience = true, // Requires the expected audience
                        ValidAudience = projectId, 
                        ValidateLifetime = true // Rejects expired tokens
                    };
                });

            builder.Services.AddCors(); // Blocks different domains calling the API unless permitted
            builder.Services.AddAuthorization();
            builder.Services.AddControllers();
            builder.Services.AddOpenApi();

            var app = builder.Build();

            // Configures the HTTP request pipeline (middleware pipeline)
            // Services registered above are consumed by middleware or controllers here

            if (app.Environment.IsDevelopment())
            {
                app.MapOpenApi();
            }

            app.UseHttpsRedirection(); // Redirects HTTP -> HTTPS

            app.UseCors(policy => policy
                .WithOrigins("http://localhost:4200") // Permits Angular frontend origin (scheme, host, port)
                .AllowAnyHeader()
                .AllowAnyMethod()); // GET/POST/PUT/DELETE etc

            app.UseAuthentication(); // Parses & validates the JWT, builds HttpContext.User
            app.UseAuthorization(); // Enforces [Authorize] attributes & policies against HttpContext.User


            app.MapControllers(); // Maps attribute-routed controllers ([Route("api/...")])

            app.Run();
        }
    }
}
