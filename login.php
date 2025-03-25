<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Exécution du script Python en passant l'email et le mot de passe
    $is_authorized = trim(shell_exec("C:\Users\coren\AppData\Local\Programs\Python\Python312\python.exe redis_client.py " . escapeshellarg($email) . " " . escapeshellarg($password) . " 2>&1"));
    echo "Résultat du script Python : " . $is_authorized;  // Afficher le résultat pour le débogage

    
    // Vérification de la sortie du script Python
    if ($is_authorized === "authorized") {
        $_SESSION['user'] = $email;
        header('Location: accueil.php');
        exit;
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
