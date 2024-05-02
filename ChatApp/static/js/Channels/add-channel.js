// チャンネルを登録する時の処理
const addChannelModal = document.getElementById("add-channel-modal");
const addPageButtonClose = document.getElementById("add-page-close-button");
const addChannelConfirmButton = document.getElementById(
  "add-channel-confirmation-button"
);

// ボタン要素を取得
const addChannelButton = document.getElementById('add-channel-button');

// クリックイベントリスナーを追加
addChannelButton.addEventListener('click', () => {
    addChannelModal.style.display = "flex";
});

// モーダル内のXボタンが押された時にモーダルを非表示にする
addPageButtonClose.addEventListener("click", () => {
  addChannelModal.style.display = "none";
});

// 画面のどこかが押された時にモーダルを非表示にする
addEventListener("click", (e) => {
  if (e.target == addChannelModal) {
    addChannelModal.style.display = "none";
  }
});

addChannelConfirmButton.addEventListener("click", () => {
    document.addChannelForm.submit();
});