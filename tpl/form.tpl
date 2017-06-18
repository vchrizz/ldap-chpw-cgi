<form action="{$formaction}" method="post">
    <div id="PasswordForm">
        <p><label for="accountname">E-Mail-Adresse:</label>
        <input type="text" name="accountname" id="accountname" required></p>
        <p><label for="oldpass">Altes Passwort:</label>
        <input type="password" name="oldpass" id="oldpass" required></p>
        <p><label for="newpass">Neues Passwort:</label>
        <input type="password" name="newpass" id="newpass" required></p>
        <p><label for="newpass2">Neues Passwort nochmals:</label>
        <input type="password" name="newpass2" id="newpass2" required></p>
        <p><input type="submit" name="submit" value="Passwort ändern"></p>
    </div>
</form>
