<?php
session_start();
if (!isset($_SESSION['user'])) {
    header('Location: login.php');
    exit;
}
$books = [
    ["titre" => "Livre A", "prix" => "10€"],
    ["titre" => "Livre B", "prix" => "15€"]
];
?>
<!DOCTYPE html>
<html>
<head>
    <title>Services</title>
</head>
<body>
    <h1>Livres disponibles</h1>
    <ul>
        <?php foreach ($books as $book): ?>
            <li><?= htmlspecialchars($book['titre']) ?> - <?= htmlspecialchars($book['prix']) ?></li>
        <?php endforeach; ?>
    </ul>
    <a href="accueil.php">Retour à l'accueil</a>
</body>
</html>