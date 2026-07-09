# 推荐
- 推荐用Task命令+程序命令+pipe/event优雅关闭
- 不推荐直接把可执行文件作为程序命令，因为这样会出现窗口
	- `-ldflags "-H windowsgui"`，标记是gui程序，不会弹出窗口，但是标准错误、标准输出可能会因为某些库不用os.Stdout,os.Stderr而导致丢失，丢失未捕获的panic信息
	- 在程序命令中wait也不行，这样窗口不会关闭，不是`-WindowStyle Hidden`也是会有窗口
		- 此时关闭窗口可以接受到中断信号
	- 以后台方式运行
		- 这样无法接受窗口关闭通知，后台本就无法接受console的ctrl+c通知，只能用其他方式来实现，即pipe/event



# Task Schedule
- 过了计划时间立即启动任务：必须是时间计划才可以，登录计划不行

## pw管理

### Task命令

```powershell
# ── 配置 ──────────────────────────────────────────────
$TaskName = "xxxx"
$command = "./serv.ps1"
$WorkDir = $PWD
# ──────────────────────────────────────────────────────

function Register-Task {
    $action = New-ScheduledTaskAction `
        -Execute  "powershell.exe" `
        -Argument "-ExecutionPolicy Bypass -Command `"Set-Location '$WorkDir'; & $command start`""

    $trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

    $settings = New-ScheduledTaskSettingsSet `
        -StartWhenAvailable `
        -ExecutionTimeLimit ([TimeSpan]::Zero)

    $principal = New-ScheduledTaskPrincipal `
        -UserId    ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) `
        -LogonType Interactive `
        -RunLevel  Highest

    Register-ScheduledTask `
        -TaskName  $TaskName `
        -Action    $action `
        -Trigger   $trigger `
        -Settings  $settings `
        -Principal $principal `
        -Force

    Write-Host "✅ 注册成功：$TaskName"
}

function Start-Task {
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "▶ 已启动：$TaskName"
}

function Stop-Task {
    Stop-ScheduledTask -TaskName $TaskName
    Write-Host "⏹ 已停止：$TaskName"
    try {
        Write-Host "⏳ 尝试关闭程序..."
        & $command stop
        Write-Host "✅ 关闭程序命令已执行"
    }
    catch {
        Write-Host "❌ 关闭程序失败：$($_.Exception.Message)"
    }
}


function Restart-Task {
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Start-ScheduledTask -TaskName $TaskName
    Write-Host "🔄 已重启：$TaskName"
}

function Get-TaskStatus {
    $t = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if (-not $t) { Write-Host "❌ 任务不存在：$TaskName"; return }

    $info = Get-ScheduledTaskInfo -TaskName $TaskName

    $stateStr = $t.State.ToString()
    if ($stateStr -eq "Ready") { $stateLabel = "⏸ 准备就绪（未运行）" }
    elseif ($stateStr -eq "Running") { $stateLabel = "▶ 运行中" }
    elseif ($stateStr -eq "Disabled") { $stateLabel = "🚫 已禁用" }
    elseif ($stateStr -eq "Queued") { $stateLabel = "⏳ 排队中" }
    else { $stateLabel = "❓ $stateStr" }

    if ($info.LastTaskResult -eq 0) {
        $resultLabel = "✅ 成功"
    }
    else {
        $resultLabel = "⚠ 代码 $($info.LastTaskResult)"
    }

    Write-Host "任务名称 : $($t.TaskName)"
    Write-Host "状态     : $stateLabel"
    Write-Host "上次运行 : $($info.LastRunTime)"
    Write-Host "上次结果 : $resultLabel"
    Write-Host "下次运行 : $($info.NextRunTime)"

    try {
        Write-Host ""
        Write-Host ""
        Write-Host "$command status："
        & $command status
        Write-Host "✅ status已执行"
    }
    catch {
        Write-Host "❌ 执行status命令失败：$($_.Exception.Message)"
    }
}

function Remove-Task {
    $t = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if (-not $t) { Write-Host "任务不存在：$TaskName"; return }
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "🗑 已删除：$TaskName"
}


function Invoke-Elevated {
    param(
        [string]$WorkDir,
        [string]$ScriptPath,
        [array]$Arguments
    )
    # 1. 检测当前是否为管理员权限
    $currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    $isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
  
    # 2. 非管理员则自动提权重启脚本
    if (-not $isAdmin) {
        Write-Host "⚠ 当前权限不足，正在尝试以管理员身份重新运行..." -ForegroundColor Yellow
        $cmd = @"
cd "$WorkDir"; & '$ScriptPath' $($Arguments -join " ");
"@
        $escapedCmd = $cmd -replace '"', '\"'
        $arguments = @(
            "-NoExit",
            "-NoProfile",
            "-ExecutionPolicy Bypass",
            "-Command", "`"$escapedCmd`""
        ) -join " "
    
        # 创建管理员权限的进程启动信息
        $processStartInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processStartInfo.FileName = "powershell.exe"
        $processStartInfo.Arguments = $arguments
        $processStartInfo.Verb = "runas"  # 关键：指定以管理员身份运行
        $processStartInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Normal
        try {
            # 启动提权进程，会弹出UAC用户账户控制弹窗
            [System.Diagnostics.Process]::Start($processStartInfo) | Out-Null
        }
        catch {
            Write-Host "❌ 提权失败！你拒绝了管理员权限请求，脚本无法执行。" -ForegroundColor Red
            Pause
            exit 1
        }
        # 原非管理员进程退出，仅保留提权后的新进程
        exit 0
    }
}

function Enable-TaskSchedulerLogging {
    try {
        wevtutil set-log Microsoft-Windows-TaskScheduler/Operational /enabled:true
        Write-Host "✅ 已启用任务计划程序日志记录"
    }
    catch {
        Write-Host "⚠ 无法启用日志记录：$_" -ForegroundColor Yellow
    }
}
function Disable-TaskSchedulerLogging {
    try {
        wevtutil set-log Microsoft-Windows-TaskScheduler/Operational /enabled:false
        Write-Host "✅ 已禁用任务计划程序日志记录"
    }
    catch {
        Write-Host "⚠ 无法禁用日志记录：$_" -ForegroundColor Yellow
    }
}


Invoke-Elevated -WorkDir $PWD -ScriptPath $MyInvocation.MyCommand.Path -Arguments $args

# ── 入口 ───────────────────────────────────────────────
switch ($args[0]) {
    "install" { Register-Task }
    "start" { Start-Task }
    "stop" { Stop-Task }
    "restart" { Restart-Task }
    "status" { Get-TaskStatus }
    "uninstall" { Remove-Task }
    "log" { Enable-TaskSchedulerLogging }
    "nolog" { Disable-TaskSchedulerLogging }
    default {
        Write-Host "用法: .\manage.ps1 [install|start|stop|restart|status|uninstall|log|nolog]"
    }
}

```


### 程序命令

```powershell
# ── 配置 ──────────────────────────────────────────────
$exePath = ".\social_media_server.exe"
$exeName = (Get-Item $exePath).BaseName
$logRootDir = "logs\std"
# ──────────────────────────────────────────────────────

function Start-Serv {
    param(
        [switch]$wait = $false
    )
    # 检查是否已在运行
    $existing = Get-Process -Name $exeName -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "⚠ 程序已在运行中（PID: $($existing.Id)），跳过启动"
        return
    }

    # 2. 自动创建日志目录（不存在则创建，避免报错）
    if (-not (Test-Path -Path $logRootDir)) {
        New-Item -Path $logRootDir -ItemType Directory -Force | Out-Null
        Write-Host "日志目录已创建：$logRootDir"
    }

    # 3. 校验可执行文件是否存在（避免启动失败）
    if (-not (Test-Path -Path $exePath -PathType Leaf)) {
        Write-Error "错误：可执行文件不存在 → $exePath"
        exit 1
    }

    # # 扩展：自动清理7天前的日志（可选）
    # $maxLogAge = 7  # 保留7天内的日志
    # Get-ChildItem -Path $logRootDir -Filter "*.log" | Where-Object {
    #     $_.LastWriteTime -lt (Get-Date).AddDays(-$maxLogAge)
    # } | Remove-Item -Force -ErrorAction SilentlyContinue
    # Write-Host "已清理 $maxLogAge 天前的旧日志"

    # 4. 启动程序（后台运行，重定向日志）
    $timestamp = Get-Date -Format "yyyy-MM-dd"  # 生成时间戳（精确到秒）
    $stdoutLog = Join-Path -Path $logRootDir -ChildPath "${timestamp}_output.log"
    $stderrLog = Join-Path -Path $logRootDir -ChildPath "${timestamp}_error.log"
    try {
        $proc = Start-Process -FilePath $exePath `
            -RedirectStandardOutput $stdoutLog `
            -RedirectStandardError $stderrLog `
            -WindowStyle Hidden `
            -PassThru

        Write-Host "✅ 程序已后台启动"
        Write-Host "标准输出日志：$stdoutLog"
        Write-Host "错误输出日志：$stderrLog"

        if ($wait) {
            Write-Host "⏳ 等待程序退出..."
            $proc.WaitForExit()
            Write-Host "程序已退出，退出代码：$($proc.ExitCode)"
        }
    }
    catch {
        Write-Error "程序启动失败：$_"
        exit 1
    }
}


function Stop-Serv {
    param(
        [switch]$f
    )

    $procs = Get-Process -Name $exeName -ErrorAction SilentlyContinue
    if ($procs.Count -eq 0) {
        Write-Host "⚠ 程序未在运行"
        return
    }
    foreach ($proc in $procs) {
        if ($f) {
            $proc | Stop-Process -Force
            Write-Host "⏹ 已强制终止：$exeName（PID: $($proc.Id)）"
            continue
        }
        $waitGracefulShutdown = $false
        try {
        
            # 尝试优雅关闭
            # -WindowStyle必须不是Hidden, 比如Minimized
            # $proc.CloseMainWindow() | Out-Null

            $eventName = "SIGTERM_$($proc.Id)"
            # $event = [System.Threading.EventWaitHandle]::OpenExisting($eventName)
            # $event.Set()
            # $event.Close()
    
            $pipe = New-Object System.IO.Pipes.NamedPipeClientStream(".", $eventName, [System.IO.Pipes.PipeDirection]::Out)
            $pipe.Connect(1000)
            $pipe.Close()
            $waitGracefulShutdown = $true
        }
        catch [System.TimeoutException] {
            Write-Host "❌ 连接超时，程序可能未监听关闭信号"
        }
        catch [System.IO.IOException] {
            Write-Host "❌ 管道不存在，程序可能未启动或不支持优雅关闭"
        }
        catch {
            Write-Host "❌ 发送关闭信号失败：$($_.Exception.Message)"
        }


        if ($waitGracefulShutdown) {
            $maxWait = 15
            for ($i = 1; $i -le $maxWait; $i++) {
                if ($proc.HasExited) { break }
                Write-Host "⏳ 第 $i/$maxWait 次等待（1秒）..."
                Start-Sleep -Seconds 1
            }
        }
        if (-not $proc.HasExited) {
            if ($waitGracefulShutdown) {
                Write-Host "⚠ 程序未响应，强制终止..."
            }
            $proc | Stop-Process -Force
        }
        $proc.WaitForExit(5000) | Out-Null
        Write-Host "⏹ 已停止：$exeName"
    }
}

function Restart-Serv {
    param(
        [switch]$f
    )

    $procs = Get-ServProc

    foreach ($proc in $procs) {
        if ($proc) {
            Stop-Serv -f:$f
        }
    }
    Start-Serv
}

function Get-ServStatus {
    $procs = Get-Process -Name $exeName -ErrorAction SilentlyContinue
    if ($procs.Count -eq 0) {
        Write-Host "⏹ 未运行`n"
        return
    }

    # 遍历所有进程（支持多个）
    foreach ($proc in $procs) {
        try {
            $elapsed = (Get-Date) - $proc.StartTime
            Write-Host "▶ 运行中"
            Write-Host "PID      : $($proc.Id)"
            Write-Host "启动时间 : $($proc.StartTime)"
            Write-Host "已运行   : $([int]$elapsed.TotalHours) 小时 $($elapsed.Minutes) 分钟"
            Write-Host "内存占用 : $([math]::Round($proc.WorkingSet64 / 1MB, 1)) MB`n"
        }
        catch {
            Write-Host "▶ 进程 PID $($proc.Id) 无法获取启动时间（可能权限不足）`n"
        }
    }
}

# ── 入口 ───────────────────────────────────────────────
switch ($args[0]) {
    "start" { Start-Serv }
    "startw" { Start-Serv -wait }
    "stop" { Stop-Serv -f:($args -contains "-f") }
    "restart" { Restart-Serv -f:($args -contains "-f") }
    "status" { Get-ServStatus }
    default {
        Write-Host "用法: .\start.ps1 [start|startw|stop|restart|status] [-f]"
    }
}
```

# Service
- https://github.com/winsw/winsw
	- 仅XML、YAML配置文件
	- 使用方式很别扭，必须将配置文件与winsw可执行文件同名且同目录
	- 应用程序名、winsw可执行文件名、winsw文件名，有一个改变了路径都得重新安装
		- 应该是只要服务id、name有一个不变即可
		- 本质上就是winsw本身作为服务注册，应用以winsw子进程的方式启动
- https://github.com/kirillkovalenko/nssm
	- 仅GUI配置

## 坑点
- 只能用系统环境变量
- 启动的浏览器基本不以无头模式运行，也不会出现UI界面
- 定时任务会在重启后以0点开始计时继续执行
- 好像是恢复进程的运行，而不会重新启动
## winsw
- 时间+大小轮转实现有bug，必须在设定时间后才会轮转，推荐仅用时间轮转
- 如果依赖其他服务，要设置depend，除非服务会尝试一定时间的自动重试
- 启动时，可能读取到错误的时间（好像只是0点），可以尝试设置delayedAutoStart，或者尝试程序手动一定延时

```xml
<service>
    <!-- 服务 ID 和显示名称 -->
    <id>ServiceId</id>
    <name>Service Name</name>
    <description>Service description</description>

    <!-- 可执行文件和工作目录 -->
    <executable>D:\path\app.exe</executable>
    <workingdirectory>D:\ws</workingdirectory>
    <stoptimeout>30 sec</stoptimeout>
    
    <delayedAutoStart>true</delayedAutoStart>  
	<depend>mysql</depend>

    <!-- 输出日志配置 -->
    <logpath>D:\path\logs\std</logpath>
    <logname>logFilename</logname> 
	<log mode="roll-by-size">  
		<sizeThreshold>10240</sizeThreshold> <!-- 单位 KB -->  
		<keepFiles>7</keepFiles>  
	</log>

    <!-- 崩溃自动重启 -->
    <onfailure action="restart" delay="5000" />
</service>
```