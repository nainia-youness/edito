<div class="">
    <!DOCTYPE html>
</div>
<html lang="en" class="">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <h1>php code<h1>
            <?php
            /*==============================Connexion========================================*/

            $url = "http://13.37.208.5";
            $db = "SLM_PROD_30_07";

            $username = "n.youness";
            $password = "youness123";

            require_once('ripcord-master/ripcord.php');

            $common = ripcord::client($url . '/xmlrpc/2/common');
            $uid = $common->authenticate($db, $username, $password, array());
            $models = ripcord::client("$url/xmlrpc/2/object");
            /*==============================SEARCH========================================*/
            // La methode 'search'
            // Nom de colis iris.ma ZSGMETPV
            // Nom de colis Avito Z6B8IFJZ

            // Pour récupérer l'identifiant du client connecté 
            $partner = $models->execute_kw($db, $uid, $password, 'res.users', 'read', array($uid), array('fields' => array('partner_id')));
            $partner_id = $partner[0]["partner_id"][0];

            // Recuperer le parent du client s'il existe 
            $parent = $models->execute_kw($db, $uid, $password, 'res.partner', 'read', array($partner_id), array('fields' => array('parent_id')));
            $parent = $parent[0]["parent_id"][0];

            $customers = array($partner_id);
            if ($parent) {
                array_push($customers, $parent);
            }

            // Les clients possibles pour le colis 
            print_r($customers);

            // Les donnees a afficher 
            $to_print = array('fields' => array('name', 'weight', 'expeditor_id', 'source_id', 'destinator_id', 'destination_id', 'return_amount'), 'limit' => 5);

            // Recuperer les colis 
            $my_colis = $models->execute_kw($db, $uid, $password, 'sochepress.customer.request.line', 'search_read', array(array(array('customer_id', 'in', $customers))), $to_print);


            // Tester la methdoe 'search'
            // echo json_encode($colis);
            echo json_encode($my_colis);

            // Tester la methode 'read'
            // echo json_encode($partnerss);
            ?>
</body>

</html>