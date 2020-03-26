<?php

$conn = pg_connect("dbname=payroll user=postgres") or die("Could not connect");

?>

<?php
if (!isset($_POST['s'])) {
?>
<center>
<form action="" method="post">
<h2>Payroll Login</h2>
<table style="border-radius: 25px; border: 2px solid black; padding: 20px;">
    <tr>
        <td>User</td>
        <td><input type="text" name="user"></td>
    </tr>
    <tr>
        <td>Password</td>
        <td><input type="password" name="password"></td>
    </tr>
    <tr>
       <td><input type="submit" value="OK" name="s">
    </tr>
</table>
</form>
</center>
<?php
}
?>

<?php
if($_POST['s']){
    $user = $_POST['user'];
    $pass = $_POST['password'];
    $sql = "select username, first_name, last_name, salary from users where username = '$user' and password = '$pass';";
    $response = pg_query($conn, $sql);
    $result = pg_fetch_all($response);

    echo "<center>";
    echo "<h2>Welcome, " . $user . "</h2><br>";
    echo "<table style='border-radius: 25px; border: 2px solid black;' cellspacing=30>";
    echo "<tr><th>Username</th><th>First Name</th><th>Last Name</th><th>Salary</th></tr>";
    if ($result){
	for ($i = 0; $i < count($result); $i++){
	     echo "<tr>";
	     echo "<td>" . $result[$i][username] . "</td>";
	     echo "<td>" . $result[$i][first_name] . "</td>";
	     echo "<td>" . $result[$i][last_name] . "</td>";
	     echo "<td>" . $result[$i][salary] . "</td>";
	     echo "</tr>";
	}
    }
    echo "</table></center>";
    pg_close($conn);
}
?>


