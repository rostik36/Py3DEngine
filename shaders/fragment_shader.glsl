#version 330 core

struct DirectionalLight {
    vec3 direction;
    vec3 color;
};

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

uniform DirectionalLight sunlight;
uniform Material material;
uniform vec3 viewPos;

in vec3 FragPos;
in vec3 Normal;

out vec4 FragColor;

void main()
{
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(-sunlight.direction); // Sunlight direction

    // Ambient light
    vec3 ambient = material.ambient * sunlight.color;

    // Diffuse light (Lambertian reflection)
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = material.diffuse * diff * sunlight.color;

    // Specular highlights (Phong)
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = material.specular * spec * sunlight.color;

    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, 1.0);
}
