#version 330 core
layout (location = 0) in vec3 aPos; // Position

out vec3 fragColor;

uniform vec3 objectColor; // Unique color per object

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    fragColor = objectColor;  // Assign uniform color to each object
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}