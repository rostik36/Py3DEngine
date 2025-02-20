# Explain about mesh functions

### Function Signature
```
void glVertexAttribPointer(
    GLuint index,         // Attribute index (layout location)
    GLint size,           // Number of components per attribute
    GLenum type,          // Data type of each component
    GLboolean normalized, // Should fixed-point values be normalized?
    GLsizei stride,       // Byte offset between consecutive attributes
    const void *pointer   // Offset of the first component in the buffer
);
```

## 1️⃣ Position Attribute

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0));
glEnableVertexAttribArray(0);



Explanation of Parameters
|Parameter	|Value	|Meaning
| --------- |:-----| :-----|
|index	|0	|This is attribute **0**, meaning this corresponds to **position (x, y, z)** in the vertex shader.
|size	|3	|Each position consists of **3 floats**: (x, y, z).
|type	|`GL_FLOAT`	|The data type of each component is **float (4 bytes each)**.
|normalized	|`GL_FALSE`	|Data **is not normalized** (only applies to integer types).
|stride	|6 * 4	|Each vertex consists of **6 floats**: (x, y, z, nx, ny, nz), where each float takes **4 bytes**.
|pointer	|ctypes.c_void_p(0)	|The position data starts **at the beginning** of the vertex buffer (offset = 0).

### Why 6 * 4?

- Each vertex contains **position (x, y, z) and normal (nx, ny, nz)**.
- Since each float is **4 bytes**, the total size of one vertex is:
```
6 * 4 = 24 bytes
```
- This tells OpenGL that the next position value is **24 bytes after the current one** (moving to the next vertex).


## 2️⃣ Normal Attribute
```
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(12));
glEnableVertexAttribArray(1);
```
Explanation of Parameters
|Parameter	|Value	|Meaning
| --------- |:-----| :-----|
|index	|1	|This is attribute **1**, meaning this corresponds to **normal (nx, ny, nz)** in the vertex shader.
|size	|3	|Each normal consists of **3 floats**: (nx, ny, nz).
|type	|`GL_FLOAT`	|The data type of each component is **float (4 bytes each)**.
|normalized	|`GL_FALSE`	|Data **is not normalized**.
|stride	|6 * 4	|Each vertex consists of **6 floats** (position + normal), so the spacing is the same as for position.
|pointer	|ctypes.c_void_p(12)	|The normal data **starts 12 bytes after** the position data.

### Why ctypes.c_void_p(12)?

- The **first 3 floats** (x, y, z) take:
```
3 * 4 = 12 bytes
```
- The normal values **start immediately after** the position values.








### **Vertex Shader and Fragment Shader: Purpose and Execution Order**

In the graphics pipeline, **shaders** are small programs that run on the GPU to process and render 3D objects. The two most fundamental types of shaders in modern OpenGL (and Vulkan, Direct3D, etc.) are the **Vertex Shader** and the **Fragment Shader**. Each serves a specific purpose in the rendering process.

---

### **1. Vertex Shader**
#### **Purpose:**
- Processes each **vertex** of a 3D model.
- Transforms the vertex **position** from **object space** to **screen space**.
- Computes and passes data (such as color, normal vectors, texture coordinates, etc.) to the **Fragment Shader**.

#### **Execution Order:**
1. The **vertex shader** runs **once per vertex** in a 3D model.
2. It calculates the **position** of each vertex in clip space (using the **MVP matrix**).
3. It passes interpolated data (like color, texture coordinates, normals) to the next stage.

#### **Example of a Vertex Shader in GLSL:**
```glsl
#version 330 core
layout(location = 0) in vec3 position;  // Vertex position (input)
layout(location = 1) in vec3 normal;    // Normal vector (input)
layout(location = 2) in vec2 texCoord;  // Texture coordinates (input)

uniform mat4 modelViewProjection; // MVP matrix

out vec2 fragTexCoord;  // Pass to Fragment Shader
out vec3 fragNormal;    // Pass to Fragment Shader

void main() {
    gl_Position = modelViewProjection * vec4(position, 1.0);
    fragTexCoord = texCoord;
    fragNormal = normal;
}
```

---

### **2. Fragment Shader (Pixel Shader)**
#### **Purpose:**
- Runs for each **pixel** that will be drawn on the screen.
- Determines the **final color** of the pixel by using interpolated data from the **Vertex Shader**.
- Applies **textures, lighting, shading, and effects**.

#### **Execution Order:**
1. Runs **once per fragment (potential pixel)** after rasterization.
2. Uses interpolated values from the **Vertex Shader** to compute the final color.
3. Outputs the **final color** of the pixel.

#### **Example of a Fragment Shader in GLSL:**
```glsl
#version 330 core
in vec2 fragTexCoord;  // Received from Vertex Shader
in vec3 fragNormal;    // Received from Vertex Shader

out vec4 FragColor;    // Output color

uniform sampler2D texture1;  // Texture

void main() {
    vec4 texColor = texture(texture1, fragTexCoord);
    FragColor = texColor; // Output final color
}
```

---

### **Execution Order in the Pipeline:**
1. **Vertex Shader:** Runs for each vertex.
2. **Primitive Assembly & Clipping:** Vertices are grouped into **triangles**, **clipped**, and prepared for rasterization.
3. **Rasterization:** Triangles are converted into **fragments** (potential pixels).
4. **Fragment Shader:** Runs for each fragment.
5. **Depth & Blending Tests:** Determines if the fragment is visible or should be discarded.

---

### **Key Differences:**
| Feature           | Vertex Shader | Fragment Shader |
|------------------|--------------|----------------|
| Runs per...      | Vertex       | Fragment (Pixel) |
| Purpose         | Transforms vertex positions and passes data | Computes final pixel color |
| Input          | Object vertices | Interpolated data from vertex shader |
| Output         | Transformed position & data | Final pixel color |

---

### **Summary:**
- The **vertex shader** processes each **vertex** and calculates positions.
- The **fragment shader** processes each **pixel** and determines the final color.
- The **vertex shader runs first**, followed by rasterization, and then the **fragment shader runs**.

Let me know if you need more details! 🚀