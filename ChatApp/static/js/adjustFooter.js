window.addEventListener('load', function() {
  // フッターの高さを取得
  var footerHeight = document.getElementById('footer').offsetHeight;
  // bodyのpadding-bottomにフッターの高さ + 1px を設定
  document.body.style.paddingBottom = footerHeight + 1 + 'px';
});
