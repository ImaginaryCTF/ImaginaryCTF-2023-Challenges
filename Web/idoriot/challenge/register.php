<?php

session_start();

// Check if the user is already logged in
if(isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit;
}

// Check if the form is submitted
if($_SERVER['REQUEST_METHOD'] === 'POST') {

    // Initialize in-memory sqlite database schema if it doesn't exist
    $db = new PDO('sqlite:memory:');
    $db->prepare('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, user_id INTEGER)')->execute();

    // Reset the database every 30 minutes
    if(time() - filemtime('rate-limit/reset') > 1800) {
        $db->exec('DELETE FROM users WHERE user_id > 1');
        touch('rate-limit/reset');
    }

    // Add admin user if it doesn't exist
    $password = password_hash(random_bytes(32), PASSWORD_DEFAULT);
    $stmt = $db->prepare('INSERT OR IGNORE INTO users (user_id, username, password) VALUES (?, ?, ?)');
    $stmt->execute([0, 'admin', $password]);

    // Check to see if the username exists before storing it
    $username = SQLite3::escapeString($_POST['username']);
    $stmt = $db->prepare('SELECT * FROM users WHERE username = ?');

    // If the username exists, display an error message on the registration page
    if($stmt->execute([$username]) && $stmt->fetch()) {
        $errors[] = "Username already exists";
        goto error;
    } else {
        // If the user didn't pass in the user_id, Generate a random user ID
        $user_id = $_POST['user_id'] ?? random_int(1, 1000000000);

        // Store the user ID in the session
        $_SESSION['user_id'] = (int) $user_id;
        $_SESSION['expires'] = time() + 1800; // 30 minutes

        // Store the username, hashed password, and user ID in the database
        $password = password_hash($_POST['password'], PASSWORD_DEFAULT);
        $stmt = $db->prepare('INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)');
        $stmt->execute([$user_id, $username, $password]);

        // Redirect to the index
        header("Location: index.php");
        exit;
    }
}

error:
?>

<!DOCTYPE html>
<html>
<head>
    <title>Registration</title>
</head>
<body>
    <h1>Registration</h1>
    <?php if(!empty($errors)): ?>
        <ul>
            <?php foreach($errors as $error): ?>
                <li><?= $error ?></li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>

    <p>The user database will be wiped every 30 minutes.</p>
    <form method="POST" action="register.php">
        <label for="username">Username</label>
        <input type="text" name="username" id="username" required>
        <br>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <br>
        <input type="hidden" name="user_id" value="<?= random_int(1, 1000000000) ?>">
        <input type="submit" value="Register">
    </form>

    <p>Already have an account? <a href="login.php">Login</a></p>
</body>
</html>
