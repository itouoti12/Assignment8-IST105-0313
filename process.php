<?php

$macaddress = escapeshellarg($_POST['mac']);
$method = escapeshellarg($_POST['method']);

$command = escapeshellcmd("python3 network_config.py $macaddress $method");

$output = shell_exec($command);

$publicIpcmd = escapeshellcmd("ec2-metadata -v");
$publicIp = shell_exec($publicIpcmd);
$host = escapeShellarg($_SERVER['HTTP_HOST']);

echo "$output";
?>

<h2>This result was processed on my EC2 instance with Public IP:<?php echo $publicIp; ?></h2>
<h2>Access the application via Load Balancer URL: http://<?php echo $host; ?>/process.php</h2>