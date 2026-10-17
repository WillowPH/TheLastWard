/* The Patient Wing is a connected set of physical corridor sections, not seven doors pasted over one wall.
   Only first-floor navigation is affected; Chapter 2 retains its own map and rooms. */
R.wardnorth={n:'North Patient Corridor',short:'North Corridor',ch:1,x:182,y:234,dark:1,d:'The corridor narrows between patient rooms. A linen trolley has been dragged across the doors. A narrow strip of ceiling lights flickers, failing to dispel the shadows along the baseboards.',o:[
 ['northBoard','Patient transfer notice','▤','A transfer list has been scratched over with red ink.',{look:1,th:'Someone tried to move the patients after containment began. They were stopped.'}],
 ['northTrolley','Linen trolley','▣','The doors of the trolley have been tied shut with bandages.',{look:1,th:'Nothing inside is moving now.'}]
]};
R.wardservice={n:'Patient Service Crossroads',short:'Service Crossing',ch:1,x:242,y:241,dark:1,d:'The service passage runs behind the wards. A peeling evacuation diagram connects Pharmacy, Archives and Laundry. Condensation runs down a barred maintenance window.',o:[
 ['crossDiagram','Ward service map','▤','The worn map identifies the maintenance routes without revealing any new key.',{look:1,th:'The service corridor connects wards that were locked away from the public halls.'}],
 ['crossCabinet','Staff supply alcove','▣','A nearly empty cupboard contains only an old logbook.',{look:1,th:'Supplies were removed before the staff were ordered to stay inside.'}],
 ['crossHide','Supply recess','▥','A place to crouch behind stacked crates.',{act:'hide'}]
]};
// Preserve all destinations and their individual lock requirements while making a physically believable ward network.
for(const id of ['wr','wi']){if(D[id].a==='ward')D[id].a='wardnorth';else if(D[id].b==='ward')D[id].b='wardnorth'}
for(const id of ['wa','wp','wl']){if(D[id].a==='ward')D[id].a='wardservice';else if(D[id].b==='ward')D[id].b='wardservice'}
// Surgery already connects through the Laundry & Service Wing. Remove a redundant seventh ward doorway.
delete D.ws;
D.northPassage={a:'ward',b:'wardnorth'};
D.servicePassage={a:'wardnorth',b:'wardservice'};
// Chapter 2 laboratories are reached from containment below, not via hidden first-floor generator shortcuts.
delete D.gl;delete D.gp;
