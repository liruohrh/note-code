- 内存
	- 模型参数：`7B+BF16=70亿*2B ~= 13GB`+ 一些额外数据大概可能15GB
	- KV Cache


| 模型  | FP16/BF16 |    Q8 |      Q6 |      Q5 |     Q4 |      Q3 |     Q2 |
| --- | --------: | ----: | ------: | ------: | -----: | ------: | -----: |
| 1B  |      2 GB |  1 GB |  0.8 GB |  0.7 GB | 0.6 GB | 0.45 GB | 0.3 GB |
| 2B  |      4 GB |  2 GB |  1.6 GB |  1.4 GB | 1.2 GB |  0.9 GB | 0.6 GB |
| 3B  |      6 GB |  3 GB |  2.4 GB |  2.1 GB | 1.8 GB |  1.4 GB | 0.9 GB |
| 7B  |     14 GB |  7 GB |  5.8 GB |  5.0 GB | 4.4 GB |  3.5 GB | 2.6 GB |
| 8B  |     16 GB |  8 GB |  6.6 GB |  5.7 GB | 5.0 GB |  4.0 GB | 3.0 GB |
| 9B  |     18 GB |  9 GB |  7.4 GB |  6.5 GB | 5.6 GB |  4.5 GB | 3.3 GB |
| 13B |     26 GB | 13 GB | 10.8 GB |  9.4 GB | 8.2 GB |  6.5 GB | 4.8 GB |
| 14B |     28 GB | 14 GB | 11.6 GB | 10.1 GB | 8.8 GB |  7.0 GB | 5.2 GB |
| 32B |     64 GB | 32 GB |   26 GB |   23 GB |  20 GB |   16 GB |  12 GB |
| 70B |    140 GB | 70 GB |   58 GB |   50 GB |  44 GB |   35 GB |  26 GB |

FP16 ≈ 参数数 × 2 Byte
Q8 ≈ 参数数 × 1 Byte
Q6 ≈ 参数数 × 0.75 Byte
Q5 ≈ 参数数 × 0.625 Byte
Q4 ≈ 参数数 × 0.5 Byte


| 上下文长度 | KV Cache（约） |
| ----- | ----------: |
| 4K    |  0.3～0.6 GB |
| 8K    |    0.6～1 GB |
| 16K   |      1～2 GB |
| 32K   |      2～4 GB |
| 64K   |      4～8 GB |
| 128K  |     8～16 GB |


- 量化等级：Q4_K_M
	- Q4表示量化（Quantization）精度
	- K：新一代量化算法，旧的是0、1
	- 高精度 Tensor 的数量：S（small）、M（medium）、L（large）
	- 一般推荐用Q4_K_M

- GGUF：模型文件
	- 实际 GGUF 因为还包含元数据、嵌入层和量化块信息，可能会多占用2G内存
- llama.cpp：模型运行器
- Ollama：llama.cpp集成环境