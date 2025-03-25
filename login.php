<?php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];

    $is_authorized = shell_exec("python3 redis_client.py check " . escapeshellarg($email) . " " . escapeshellarg($password));
    
    if (trim($is_authorized) === "authorized") {
        $_SESSION['user'] = $email;
        header('Location: accueil.php');
        exit;
    } else {
        echo "Email ou mot de passe incorrect.";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Connexion</h1>
    <form method="post">
        <label>Email: <input type="email" name="email" required></label><br>
        <label>Mot de passe: <input type="password" name="password" required></label><br>
        <button type="submit">Se connecter</button>
    </form>
</body>
</html>