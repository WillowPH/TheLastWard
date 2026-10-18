/* This edition ships all room art locally. Compatibility API for legacy settings. */
(function(){'use strict';
 const settings={enabled:false,endpoint:null};
 window.WardArt={settings,urlFor:()=>'',prepare:()=>{},update:()=>{settings.enabled=false;}};
})();
