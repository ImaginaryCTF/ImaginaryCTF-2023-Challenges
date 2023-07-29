<?php

session_start();

// Check if user is logged in
if (!isset($_SESSION['user_id'])) {
    header("Location: login.php");
    exit;
}

// Logout user
session_destroy();

// Delete the user from the database
$db = new PDO('sqlite:memory:');
$stmt = $db->prepare('DELETE FROM users WHERE user_id = ?');
$stmt->execute([$_SESSION['user_id']]);

header("Location: index.php");
exit;

?>