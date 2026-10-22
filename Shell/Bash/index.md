

# 路径名展开（Pathname Expansion）、通配符展开（globbing）
- 当前会话开启 `shopt -s globstar`
- `du -sh /root/TraceEagle/* /root/TraceEagle/.[!.]* 2>/dev/null`
  - `/root/TraceEagle/*` 不对隐藏文件执行
  - 展开会立刻执行，因此不会在sudo后做
    - 因此要 `sudo bash -c 'du -sh /root/TraceEagle/* /root/TraceEagle/.[!.]* 2>/dev/null'`

  - 或者
    - `find /path/to/dir -mindepth 1 -maxdepth 1 -print0 | du -sh --files0-from=-`
    - `fd --print0 . /path/to/dir | du -ch --files0-from=- `
      - `fd --type f . /path/to/dir -X du -ch --`

- 对于du
  - 连续输出2层的 `du -xhd 2 /path`
  - `| awk -F'/' 'NF == 4'` 表示分割 / ，保留4个元素的