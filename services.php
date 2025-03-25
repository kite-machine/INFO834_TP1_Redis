<?php
session_start();

if (!isset($_SESSION['user'])) {
    header('Location: login.php');
    exit;
}

// Fonction pour exécuter le script Python et récupérer la sortie
function get_python_output($command) {
    $output = shell_exec($command);
    return trim($output);
}

$email = $_SESSION['user']; 

// Vérifier si un service a été sélectionné
if (isset($_POST['service'])) {
    $service_type = $_POST['service'];  
    
    $python_script_path = "redis_stats.py";  
    $python_exec = "C:\Users\coren\AppData\Local\Programs\Python\Python312\python.exe";  
    shell_exec("$python_exec $python_script_path $email $service_type");
    
    $message = "Service '$service_type' logué avec succès pour l'utilisateur $email";
} else {
    $message = "";
}
$python_script_path = "redis_stats.py";  
$python_exec = "C:\Users\coren\AppData\Local\Programs\Python\Python312\python.exe"; 
$recent_users = get_python_output("$python_exec $python_script_path recent_users");
$top_users = get_python_output("$python_exec $python_script_path top_users");
$most_used_service = get_python_output("$python_exec $python_script_path most_used_service");
?>

<!DOCTYPE html>
<html>
<head>
    <title>Services</title>
</head>
<body>
    <h1>Choisissez un service</h1>

    <?php if ($message): ?>
        <p><?php echo htmlspecialchars($message); ?></p>
    <?php endif; ?>

    <form method="post">
        <button type="submit" name="service" value="Vente">Service Vente</button>
        <button type="submit" name="service" value="Achat">Service Achat</button>
    </form>

    <h2>Statistiques des Services</h2>
    
    <h3>Les 10 derniers utilisateurs connectés :</h3>
    <ul>
        <?php
        $users = explode("\n", $recent_users);
        $unique_users = array_unique($users);
        sort($unique_users);
        
        // Afficher uniquement les utilisateurs non vides
        foreach ($unique_users as $user) {
            if (!empty($user)) {
                echo "<li>" . htmlspecialchars($user) . "</li>";
            }
        }
        ?>
    </ul>



    
    <h3>Le top 3 des utilisateurs les plus connectés :</h3>
        <ul>
            <?php
            $top_users = explode("\n", $top_users); 
            foreach ($top_users as $user) {
                list($email, $count) = explode(":", $user);
                echo "<li>User: " . htmlspecialchars($email) . " - Connexions: $count</li>";
            }
            ?>
        </ul>


    

    <h3>Le service le plus utilisé :</h3>
    <p><?php echo htmlspecialchars($most_used_service); ?></p>
    <a href="accueil.php">Aller à l'accueil</a>
    <a href="login.php">Déconnexion</a>
</body>
</html>
