// 与えられたページに基づいて、特定の範囲のチャンネルを表示する関数
const show = (page, step) => {
    // 開始インデックスと終了インデックスを計算
    const startIndex = (page - 1) * step;
    const endIndex = startIndex + step;
    // 範囲のログ出力
    console.log(`Displaying items from index ${startIndex} to ${endIndex - 1}`);
    // すべてのチャンネル項目を取得
    const items = document.querySelectorAll('.list-group-item');
    // 各項目に対して、表示または非表示を設定
    items.forEach((item, index) => {
        if (index >= startIndex && index < endIndex) {
            item.classList.remove('d-none');
        } else {
            item.classList.add('d-none');
        }
    });
};

// ページネーションを設定して初期化する関数
const pagination = () => {
    const channels = document.querySelectorAll('.list-group-item');
    const step = 4;
    const total = Math.ceil(channels.length / step);
    const paginationUI = document.querySelector(".pagination");

    for (let i = 1; i <= total; i++) {
        const pageNumber = document.createElement("li");
        pageNumber.className = "page-item";
        pageNumber.innerHTML = `<a class="page-link" href="#">${i}</a>`;
        if (i === 1) pageNumber.classList.add("active");
        paginationUI.insertBefore(pageNumber, paginationUI.querySelector("#next"));

        pageNumber.addEventListener("click", (e) => {
            e.preventDefault();
            document.querySelector('.pagination .active').classList.remove('active');
            pageNumber.classList.add('active');
            show(i, step);
        });
    }

    document.getElementById("prev").addEventListener("click", (e) => {
        e.preventDefault();
        let currentPage = parseInt(document.querySelector('.pagination .active a').textContent);
        if (currentPage > 1) {
            document.querySelectorAll('.pagination .page-item')[currentPage - 1].click();
        }
    });

    
    document.getElementById("next").addEventListener("click", (e) => {
        e.preventDefault();
        let currentPage = parseInt(document.querySelector('.pagination .active a').textContent);
        if (currentPage < total) {
            document.querySelectorAll('.pagination .page-item')[currentPage +1 ].click();
        }
        
    });
    
    show(1, step);
};

document.addEventListener("DOMContentLoaded", pagination);
