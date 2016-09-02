<form action="/upload" method="post" enctype="multipart/form-data">
    <dl>
        <dd>Text: <input type="input" name="category"/></dd>
        <dd>File: <input type="file" name="upload"/></dd>
        <dd><input type="submit" value="submit"/></dd>
    </dl>
</form>
% rebase('layout/layout.tpl', message=message)