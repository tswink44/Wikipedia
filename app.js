document.getElementById("startButton").addEventListener("click", async function() {
    const targetPage = await getRandomWikipediaPage();
    console.log("Target page:", targetPage);

    let clickCount = 0;
    let currentUrl = "https://en.wikipedia.org/wiki/Main_Page";

    while (currentUrl !== targetPage) {
        clickCount++;
        currentUrl = await simulateClickAndGetNextPage(currentUrl);
        console.log(`Click #${clickCount}: Now at ${currentUrl}`);
    }

    document.getElementById("output").innerText = `It took ${clickCount} clicks to reach the target page: ${targetPage}`;
});

// Fetch a random Wikipedia article
async function getRandomWikipediaPage() {
    const response = await fetch("https://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=1&format=json");
    const data = await response.json();
    const randomPageTitle = data.query.random[0].title;
    return `https://en.wikipedia.org/wiki/${randomPageTitle.replace(/ /g, "_")}`;
}

// Simulate a click on the Wikipedia page and return the next page URL
async function simulateClickAndGetNextPage(currentUrl) {
    const response = await fetch(currentUrl);
    const text = await response.text();

    // Parse the page content to find the first relevant hyperlink (skipping non-article links)
    const doc = new DOMParser().parseFromString(text, "text/html");
    const links = doc.querySelectorAll("a[href^='/wiki/']");
    const randomLink = links[Math.floor(Math.random() * links.length)];
    const nextUrl = "https://en.wikipedia.org" + randomLink.getAttribute("href");

    return nextUrl;
}

async function getPageContent(pageUrl) {
    const pageTitle = pageUrl.split("/").pop().replace(/_/g, " ");
    const response = await fetch(`https://en.wikipedia.org/w/api.php?action=query&titles=${pageTitle}&prop=links&format=json`);
    const data = await response.json();
    return data.query.pages;
}