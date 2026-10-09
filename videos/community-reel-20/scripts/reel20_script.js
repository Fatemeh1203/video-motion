    <script>
      (function () {
        const B = 0.5; // 120 BPM
        const tl = gsap.timeline({ paused: true });
        const sweep = (sel, t, d) => tl.fromTo(sel, { xPercent: -160 }, { xPercent: 320, duration: d || 0.9, ease: "power2.inOut", immediateRender: false }, t);
        const show = (sel, t) => tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: 0.01 }, t);
        const hide = (sel, t, d) => tl.to(sel, { opacity: 0, duration: d || 0.12 }, t);

        // ---- aurora drift (slow, seek-safe) + beat pulse
        tl.fromTo("#b1", { x: 0, y: 0, scale: 1 }, { x: 260, y: 220, scale: 1.15, duration: 20, ease: "sine.inOut" }, 0);
        tl.fromTo("#b2", { x: 0, y: 0, scale: 1 }, { x: -240, y: -320, scale: 1.2, duration: 20, ease: "sine.inOut" }, 0);
        tl.fromTo("#b3", { x: 0, y: 0, scale: 1.1 }, { x: 300, y: -180, scale: 0.95, duration: 20, ease: "sine.inOut" }, 0);
        tl.fromTo("#b4", { x: 0, y: 0 }, { x: -260, y: 380, duration: 20, ease: "sine.inOut" }, 0);
        for (let t = 0; t < 19; t += B) {
          const drop = t >= 10 && t < 14;
          tl.fromTo("#pulse", { opacity: drop ? 0.9 : 0.5, scale: drop ? 1.08 : 1.04 }, { opacity: 0, scale: 1, duration: 0.45, ease: "power2.out", immediateRender: false }, t);
        }

        // ---- S1 hook (0-3): visible from frame 0
        const TOOLS = [["ChatGPT", "#91ffea"], ["Claude", "#ffbf86"], ["Gemini", "#77caff"], ["Midjourney", "#b39aff"], ["Perplexity", "#91ffea"], ["NotebookLM", "#ddf998"],
          ["Cursor", "#ff94ba"], ["n8n", "#ff94ba"], ["Suno", "#ffbf86"], ["Runway", "#b39aff"], ["DeepSeek", "#77caff"], ["Canva AI", "#ddf998"], ["Copilot", "#77caff"], ["Gamma", "#91ffea"]];
        const LANES = [270, 1300, 380, 1420, 480, 1180, 330, 1360, 430, 1240, 300, 1450, 520, 1150];
        const fbox = document.querySelector("#flyers");
        TOOLS.forEach(function (t, i) {
          const el = document.createElement("div");
          el.className = "flyer glass";
          el.style.setProperty("--c", t[1]);
          el.style.top = LANES[i] + "px";
          el.style.left = "0px";
          el.innerHTML = "<i></i><span>" + t[0] + "</span>";
          fbox.appendChild(el);
          // fly across, right to left, staggered on 16ths
          const at = -0.6 + i * 0.16;
          tl.fromTo(el, { x: 1120, opacity: 1 }, { x: -420, duration: 2.0 + (i % 3) * 0.3, ease: "none" }, Math.max(0, at));
        });
        tl.fromTo("#h1", { scale: 1.12 }, { scale: 1, duration: 0.6, ease: "power3.out" }, 0);
        tl.fromTo("#h2", { opacity: 0, y: 80, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "power4.out" }, 0.5);
        tl.to("#h12", { opacity: 0, y: -80, filter: "blur(12px)", duration: 0.18, ease: "power2.in" }, 1.38);
        tl.fromTo("#h3", { opacity: 0, scale: 1.45, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "power4.out" }, 1.5);
        tl.fromTo("#stage", { x: 0, y: 0 }, { x: 10, y: -8, duration: 0.05, yoyo: true, repeat: 3, ease: "none", immediateRender: false }, 1.5);
        tl.to("#h3", { scale: 1.06, duration: 1.0, ease: "sine.in" }, 1.82);
        tl.to("#h3", { opacity: 0, scale: 1.4, filter: "blur(14px)", duration: 0.16, ease: "power2.in" }, 2.86);
        hide("#s1", 3.0, 0.02);

        // ---- S2 not alone (3-5)
        show("#s2", 3.0);
        tl.fromTo("#s2-a", { opacity: 0, scale: 0.6, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "back.out(1.6)" }, 3.0);
        gsap.utils.toArray("#s2-b .w").forEach(function (w, i) {
          tl.fromTo(w, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.25, ease: "power4.out" }, 3.5 + i * (B / 2));
        });
        tl.fromTo("#brand", { opacity: 0, y: 50, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "back.out(2)" }, 4.0);
        sweep("#brand .sheen", 4.25, 0.7);
        tl.to("#s2", { opacity: 0, scale: 0.94, filter: "blur(10px)", duration: 0.16, ease: "power2.in" }, 4.86);

        // ---- S3 every AI tool, daily lessons (5-10)
        tl.fromTo("#s3", { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power2.out" }, 5.0);
        tl.fromTo("#s3-a", { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 0.28, ease: "power4.out" }, 5.0);
        tl.fromTo("#s3-b", { opacity: 0, y: 60, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }, 5.25);
        tl.fromTo("#s3-c", { opacity: 0, y: 60, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, ease: "power4.out" }, 5.5);
        tl.fromTo("#slot", { opacity: 0, scale: 0.85 }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }, 5.75);
        const sbox = document.querySelector("#slot-names");
        TOOLS.forEach(function (t, i) {
          const el = document.createElement("div");
          el.className = "slot-name";
          el.style.color = t[1];
          el.textContent = t[0];
          sbox.appendChild(el);
          const at = 6.0 + i * (B / 2); // a new tool every eighth note
          tl.fromTo(el, { opacity: 0, y: 90 }, { opacity: 1, y: 0, duration: 0.12, ease: "power3.out" }, at);
          if (i < TOOLS.length - 1) tl.to(el, { opacity: 0, y: -90, duration: 0.1, ease: "power2.in" }, at + B / 2 - 0.1);
        });
        tl.fromTo("#s3-sub", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }, 7.0);
        gsap.utils.toArray("#s3-tags .chip").forEach(function (c, i) {
          tl.fromTo(c, { opacity: 0, y: 30, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, 7.5 + i * (B / 2));
        });
        sweep("#slot .sheen", 8.0, 0.8);
        tl.to("#slot", { scale: 1.05, duration: 0.8, ease: "sine.in" }, 9.0);
        tl.to("#s3", { opacity: 0, scale: 1.25, filter: "blur(14px)", duration: 0.16, ease: "power3.in" }, 9.84);

        // ---- S4 bento (10-14, the drop)
        tl.fromTo("#s4", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 10.0);
        tl.fromTo("#s4-head", { opacity: 0, y: -40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power4.out" }, 10.0);
        ["#t1", "#t2", "#t3", "#t4"].forEach(function (t, i) {
          tl.fromTo(t, { opacity: 0, scale: 0.8, y: 60, filter: "blur(10px)" }, { opacity: 1, scale: 1, y: 0, filter: "blur(0px)", duration: 0.35, ease: "back.out(1.8)" }, 10.0 + i * B / 2);
          sweep(t + " .sheen", 11.3 + i * 0.18, 0.8);
          tl.fromTo(t + " svg", { scale: 0.6, rotation: -12 }, { scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2.5)" }, 10.1 + i * B / 2);
        });
        tl.to(["#t1", "#t2", "#t3", "#t4"], { y: -10, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 1, stagger: 0.08 }, 12.5);
        tl.to("#s4", { opacity: 0, scale: 0.94, filter: "blur(10px)", duration: 0.16, ease: "power2.in" }, 13.84);

        // ---- S5 invite (14-20)
        show("#s5", 14.0);
        tl.fromTo("#cta-video", { opacity: 0, scale: 1.12 }, { opacity: 0.4, scale: 1, duration: 1.2, ease: "power2.out" }, 14.0);
        tl.fromTo("#s5-eye", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 14.0);
        tl.fromTo("#s5-t1", { opacity: 0, y: 70, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power4.out" }, 14.1);
        tl.fromTo("#s5-t2", { opacity: 0, y: 70, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power4.out" }, 14.35);
        tl.fromTo("#link", { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2)" }, 14.6);
        tl.fromTo("#link .plane", { rotation: -40, x: -30 }, { rotation: 0, x: 0, duration: 0.6, ease: "back.out(2.4)" }, 14.7);
        gsap.utils.toArray("#s5-tags .tag").forEach(function (t, i) {
          tl.fromTo(t, { opacity: 0, y: 24, scale: 0.85 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(2.2)" }, 15.2 + i * 0.2);
        });
        tl.fromTo("#sign", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 15.8);
        tl.fromTo("#sign i", { scaleY: 0 }, { scaleY: 1, duration: 0.4, ease: "expo.out" }, 15.95);
        tl.fromTo("#comment", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }, 16.4);
        sweep("#link .sheen", 15.6, 0.9);
        sweep("#link .sheen", 17.6, 0.9);
        tl.fromTo("#link", { boxShadow: "inset 0 1.5px 0 rgba(255,255,255,0.35), 0 0 70px rgba(137,255,240,0.35)" }, { boxShadow: "inset 0 1.5px 0 rgba(255,255,255,0.35), 0 0 120px rgba(137,255,240,0.7)", duration: 1.0, ease: "sine.inOut", yoyo: true, repeat: 2, immediateRender: false }, 16.0);
        tl.to("#s5-copy, #link, #s5-tags, #sign, #comment", { opacity: 0, duration: 0.3, ease: "power1.in" }, 19.7);

        window.__timelines = window.__timelines || {};
        window.__timelines["main"] = tl;
      })();
    </script>
  </body>
</html>
