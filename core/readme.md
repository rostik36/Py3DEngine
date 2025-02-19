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