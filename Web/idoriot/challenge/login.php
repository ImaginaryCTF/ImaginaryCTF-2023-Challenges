<?php

session_start();

// Check if user is already logged in
if (isset($_SESSION['user_id'])) {
    header("Location: index.php");
    exit;
}

if (!isset($_SESSION['expires'])) {
    $_SESSION['expires'] = time() + 1800; // 30 minutes
}

// Check if form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {

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

    // Validate form data
    $errors = [];
    if (empty($_POST['username'])) {
        $errors[] = "Username is required";
        goto error;
    }
    if (empty($_POST['password'])) {
        $errors[] = "Password is required";
        goto error;
    }

    // Check if username and password are valid
    $username = SQLite3::escapeString($_POST['username']);
    $password = $_POST['password'];

    // Prepare query
    $stmt = $db->prepare('SELECT * FROM users WHERE username = ?');
    $stmt->execute([$username]);
    $user = $stmt->fetch();

    // Check if username matches password hash
    if ($user && password_verify($password, $user['password'])) {
        // Login successful
        // Store user ID in session
        $_SESSION['user_id'] = (int) $user['user_id'];

        // Redirect to landing page, pass user ID in URL
        header("Location: index.php");
        exit;
    } else {
        // Login failed
        $errors[] = "Failed to log in";
        goto error;
    }
error:
}

?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>

    <?php if (!empty($errors)) : ?>
        <div style="color: red;">
            <?php foreach ($errors as $error) : ?>
                <p><?php echo $error; ?></p>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>

    <form method="POST" action="">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div>
            <button type="submit">Login</button>
        </div>
    </form>

    <p>Don't have an account? <a href="register.php">Register</a></p>
</body>
</html>
