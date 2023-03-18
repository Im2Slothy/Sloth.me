<?php
// Retrieve the contents of the JSON file into an array
$json = file_get_contents('short_urls.json');
$short_urls = json_decode($json, true);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the long URL from the form data
    $long_url = $_POST['url'];

    // Generate a random string of characters for the short URL
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $short_url = '';
    for ($i = 0; $i < 6; $i++) {
        $short_url .= $characters[rand(0, strlen($characters) - 1)];
    }

    // Set the expiration date for the short URL (1 month from today)
    $expiration_date = date('Y-m-d', strtotime('+1 month'));

    // Insert the short URL and its expiration date into the array
    $short_urls[$short_url] = [
        'long_url' => $long_url,
        'expiration_date' => $expiration_date,
    ];

    // Write the updated array back to the JSON file
    $json = json_encode($short_urls);
    file_put_contents('short_urls.json', $json);

    // Redirect the user to the newly created short URL
    header("Location: http://sloth.me/$short_url");
    exit();
}
?>
