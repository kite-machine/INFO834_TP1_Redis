<?php
session_start();
?>
<!DOCTYPE html>
<html>
<head>
    <title>Accueil</title>
</head>
<body>
    <h1>Bienvenue sur notre site de vente de livres</h1>
    <?php if (isset($_SESSION['user'])): ?>
        <p>Connecté en tant que <?= htmlspecialchars($_SESSION['user']) ?></p>
        <a href="services.php">Voir les livres</a> |
        <a href="login.php">Déconnexion</a>
    <?php else: ?>
        <a href="login.php">Connexion</a>
    <?php endif; ?>
</body>
</html>




