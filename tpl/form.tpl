<form action="{$formaction}" method="post">
    <div id="PasswordForm">
        <p><label for="accountname">Account Name:</label>
        <input type="text" name="accountname" id="accountname" placeholder="Your account name, including internal prefix" required value="{$accountname}"></p>
        <p><label for="oldpass">Old Password:</label>
        <input type="password" name="oldpass" id="oldpass" required></p>
        <p><label for="newpass">New Password:</label>
        <input type="password" name="newpass" id="newpass" required></p>
        <p><label for="newpass2">Repeat New Password:</label>
        <input type="password" name="newpass2" id="newpass2" required></p>
        <p><input type="submit" name="submit" value="Change Password"></p>
        <p><a href="https://log:out@{$http_host}/">Logout</a> (after logout click cancel and close browser/tab!)
    </div>
</form>
