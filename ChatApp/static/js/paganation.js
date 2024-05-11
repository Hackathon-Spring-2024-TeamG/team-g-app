



const pagination = async () => {
    let page = 1;
    const STEP = 4;


    const TOTAL =
        channels.length % STEP == 0
        ? channels.length / STEP
        : Math.floor(channels.length / STEP) + 1;

    const paginationUI = document.querySelector(".pagenation");
    let pageCount = 0;
    while (pageCount < TOTAL) {
        let pageNumber = document.createElement("li");
        pageNumber.dataset.pageNum = pageCount + 1;
        paginationUI.appendChild(pageNumber);

        pageNumber.addEventListener
    }
}


