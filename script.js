async function loadEvents() {
  try {
    const res = await fetch("events.json?_=" + Date.now());
    const data = await res.json();

    const container = document.getElementById("events-container");
    container.innerHTML = "";

    if (data.length === 0) {
      container.innerHTML = "<p>Nessun evento trovato al momento.</p>";
      return;
    }

    data.forEach(event => {
      const card = document.createElement("div");
      card.className = "event-card";
      card.innerHTML = `
        <h3><a href="${event.url}" target="_blank">${event.title}</a></h3>
        <p><strong>Fonte:</strong> ${event.source}</p>
      `;
      container.appendChild(card);
    });

    document.getElementById("updated").textContent = new Date().toLocaleString("it-IT");
  } catch (err) {
    console.error(err);
    document.getElementById("events-container").innerHTML = "<p>Errore nel caricamento degli eventi.</p>";
  }
}

loadEvents();
