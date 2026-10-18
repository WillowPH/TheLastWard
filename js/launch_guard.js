/* WebGL cannot upload local-file images on browsers with opaque file origins. */
(function(){'use strict';if(location.protocol!=='file:')return;
 document.addEventListener('DOMContentLoaded',()=>{
  const help=document.createElement('section');help.setAttribute('role','alert');
  help.style.cssText='position:fixed;inset:0;z-index:2147483647;display:grid;place-content:center;background:#080c0b;color:#d7d7cb;font:18px/1.7 Arial,sans-serif;padding:32px';
  help.innerHTML='<h1 style="color:#c8b38b">Start the game with its launcher</h1><p>Extract the <b>whole ZIP</b>, then double-click <b>START_GAME.exe</b> or <b>START_GAME.bat</b>.<br>The Windows launcher needs no Python and opens the game in your browser.<br>Keep its window open while playing.</p><p>Opening index.html directly prevents the panoramic room artwork from loading.<br>macOS/Linux: run <b>python3 start_game.py</b> from the extracted folder.</p>';
  document.body.append(help);
 });
})();
