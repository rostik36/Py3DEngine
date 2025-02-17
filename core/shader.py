import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


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