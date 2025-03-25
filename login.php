<?php
session_start();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $_SESSION['user'] = $_POST['username'];
    header('Location: accueil.php');
    exit;
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
        <label>Nom d'utilisateur: <input type="text" name="username" required></label>
        <button type="submit">Se connecter</button>
    </form>
</body>
</html>