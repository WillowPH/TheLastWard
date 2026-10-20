"""Shared real-pointer controls for native authored room views.

These helpers exercise the same drag gesture a player uses. They never call the
camera API or synthesize a click on a removed navigation control.
"""


def turn_room(page, direction=-1):
    page.wait_for_function(
        'WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy&&!WardWinter.travelling'
    )
    before = page.evaluate('S.roomView')
    frame = page.locator('.room-view-frame').bounding_box()
    assert frame and frame['width'] >= 120, ('Room view too small to drag', frame)
    start = .75 if direction < 0 else .25
    finish = .25 if direction < 0 else .75
    y = frame['y'] + frame['height'] * .12
    page.mouse.move(frame['x'] + frame['width'] * start, y)
    page.mouse.down()
    page.mouse.move(frame['x'] + frame['width'] * finish, y, steps=15)
    page.mouse.up()
    page.wait_for_function(
        'WardWinter.roomViewRenderer()?.loaded&&!WardWinter.orbit.busy'
    )
    assert page.evaluate('S.roomView') != before, ('A horizontal room drag did not change facing', page.evaluate('({room:S.room,view:S.roomView,hp:S.hp,paused:WardWinter.isPaused(),modal:document.querySelector("#m .md")?.innerText,focus:S.sceneFocus,hiding:S.f.hidingRoom,travelling:WardWinter.travelling,busy:WardWinter.orbit.busy,frame:document.querySelector(".room-view-frame")?.getBoundingClientRect().toJSON()})'))
    # Releasing a drag intentionally suppresses the browser's trailing click.
    # Wait for that safety interval before tests click a scene object.
    page.wait_for_timeout(420)
