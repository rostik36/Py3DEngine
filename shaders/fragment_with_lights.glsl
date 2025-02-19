#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

// Material properties
uniform vec3 material_ambient;
uniform vec3 material_diffuse;
uniform vec3 material_specular;
uniform float material_shininess;

// Light properties
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;

void main()
{
    // Normalize vectors
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    
    // Ambient component
    vec3 ambient = material_ambient * lightColor;
    
    // Diffuse component (Lambertian reflection)
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = material_diffuse * diff * lightColor;
    
    // Specular component (Phong model)
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material_shininess);
    vec3 specular = material_specular * spec * lightColor;

    // Final color with lighting
    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, 1.0);
}
