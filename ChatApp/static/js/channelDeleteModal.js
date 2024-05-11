document.addEventListener('DOMContentLoaded', function () {
  // モーダルを表示するリンクにイベントリスナーを設定
  let deleteButton = document.querySelectorAll('[data-bs-toggle="modal"]');
  deleteButton.forEach(function(btn) {
    btn.addEventListener('click', function () {
      let deleteUrl = btn.getAttribute('data-href'); // data-href属性から削除URLを取得
      document.getElementById('delete-confirmation-link').href = deleteUrl; // 「削除」リンクにURLを設定
    });
  });
});