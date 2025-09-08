async function renderSpark({endpoint}) {
  async function fetchData(){
    const res = await fetch(endpoint);
    return await res.json();
  }
  function draw(trades){
    const c = document.getElementById("spark");
    const ctx = c.getContext("2d");
    ctx.clearRect(0,0,c.width,c.height);
    if(!trades.length) return;
    const prices = trades.map(t=>t.price).reverse();
    const min = Math.min(...prices), max = Math.max(...prices);
    const pad = 6;
    const w = c.width - pad*2, h = c.height - pad*2;
    ctx.beginPath();
    prices.forEach((p,i)=>{
      const x = pad + (i/(prices.length-1))*w;
      const y = pad + (1-(p-min)/(max-min||1))*h;
      i ? ctx.lineTo(x,y) : ctx.moveTo(x,y);
    });
    ctx.lineWidth = 2; ctx.strokeStyle = "#2c7"; ctx.stroke();
  }
  const initial = await fetchData(); draw(initial);
  setInterval(async ()=>draw(await fetchData()), 15000);
}
