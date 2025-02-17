import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# Simple vertex & fragment shader source code
VERTEX_SHADER_SOURCE = """
#version 330 core
layout(location = 0) in vec3 aPos;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
void main() {
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
"""

FRAGMENT_SHADER_SOURCE = """
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
    vec3 lightDir = normalize(-sunlight.direction);  // Sunlight direction

    // Ambient light (constant, affects everything)
    vec3 ambient = material.ambient * sunlight.color;

    // Diffuse light (based on angle of incidence)
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = material.diffuse * diff * sunlight.color;

    // Specular highlights (shiny reflections)
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = material.specular * spec * sunlight.color;

    vec3 result = ambient + diffuse + specular;
    FragColor = vec4(result, 1.0);
}
"""

class Shader:
    def __init__(self, vertex_src_path, fragment_src):
        # Load shaders
        vertex_shader_source = None
        fragment_shader_source = None
        
        with open(vertex_src_path) as f:
            vertex_shader_source = f.read()
        with open(fragment_src) as f:
            fragment_shader_source = f.read()
        
        if not vertex_shader_source or not fragment_shader_source:
            raise Exception("Failed to load shaders")

        self.program = glCreateProgram()
        vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)

        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def use(self):
        glUseProgram(self.program)

    def set_uniform3fv(self, name, value):
        glUniform3fv(glGetUniformLocation(self.program, name), 1, glm.value_ptr(value))

    def set_uniform1f(self, name, value):
        glUniform1f(glGetUniformLocation(self.program, name), value)

    def set_uniform_matrix4fv(self, name, matrix):
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, glm.value_ptr(matrix))




# class Shader:
#     """Handles OpenGL shader compilation and usage."""
    
#     def __init__(self, vertex_src=VERTEX_SHADER_SOURCE, fragment_src=FRAGMENT_SHADER_SOURCE):
#         self.program = glCreateProgram()

#         # Compile vertex shader
#         vertex_shader = glCreateShader(GL_VERTEX_SHADER)
#         glShaderSource(vertex_shader, vertex_src)
#         glCompileShader(vertex_shader)
#         if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
#             raise RuntimeError(glGetShaderInfoLog(vertex_shader))

#         # Compile fragment shader
#         fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
#         glShaderSource(fragment_shader, fragment_src)
#         glCompileShader(fragment_shader)
#         if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
#             raise RuntimeError(glGetShaderInfoLog(fragment_shader))

#         # Link shaders
#         glAttachShader(self.program, vertex_shader)
#         glAttachShader(self.program, fragment_shader)
#         glLinkProgram(self.program)
#         if not glGetProgramiv(self.program, GL_LINK_STATUS):
#             raise RuntimeError(glGetProgramInfoLog(self.program))

#         glDeleteShader(vertex_shader)
#         glDeleteShader(fragment_shader)

#     def use(self):
#         """Activate the shader."""
#         glUseProgram(self.program)

#     def set_uniform_matrix4fv(self, name, matrix):
#         """Set a uniform mat4 variable."""
#         location = glGetUniformLocation(self.program, name)
#         glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(matrix))

#     def set_uniform3fv(self, name, value):
#         glUniform3fv(glGetUniformLocation(self.program, name), 1, glm.value_ptr(value))

#     def set_uniform1f(self, name, value):
#         glUniform1f(glGetUniformLocation(self.program, name), value)

#     def set_uniform_matrix4fv(self, name, matrix):
#         glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, glm.value_ptr(matrix))


    # def set_uniform3fv(self, name, value):
    #     glUniform3fv(glGetUniformLocation(self.program, name), 1, glm.value_ptr(value))

    # def set_uniform1f(self, name, value):
    #     glUniform1f(glGetUniformLocation(self.program, name), value)

    # def set_uniform_matrix4fv(self, name, matrix):
    #     glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, glm.value_ptr(matrix))

