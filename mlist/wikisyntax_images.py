#!/usr/bin/env python
# coding=utf-8

wikisyntax_images = dict({
	u'money' : u'/icons/images/money.png',
	u'monitor' : u'/icons/images/monitor.png',
	u'mouse' : u'/icons/images/mouse.png',
	u'note' : u'/icons/images/note.png',
	u'page' : u'/icons/images/page.png',
	u'pill' : u'/icons/images/pill.png',
	u'pound' : u'/icons/images/pound.png',
	u'printer' : u'/icons/images/printer.png',
	u'question' : u'/icons/images/question.png',
	u'raquet' : u'/icons/images/raquet.png',
	u'report' : u'/icons/images/report.png',
	u'ruby' : u'/icons/images/ruby.png',
	u'shield' : u'/icons/images/shield.png',
	u'shuttlecock' : u'/icons/images/shuttlecock.png',
	u'soccer' : u'/icons/images/soccer.png',
	u'star' : u'/icons/images/star.png',
	u'stop' : u'/icons/images/stop.png',
	u'telephone' : u'/icons/images/telephone.png',
	u'tennis' : u'/icons/images/tennis.png',
	u'tick' : u'/icons/images/tick.png',
	u'time' : u'/icons/images/time.png',
	u'trash' : u'/icons/images/trash.png',
	u'tree' : u'/icons/images/tree.png',
	u'tv' : u'/icons/images/tv.png',
	u'user' : u'/icons/images/user_male.png',
	u'user:female' : u'/icons/images/user_female.png',
	u'user:gray' : u'/icons/images/user_gray.png',
	u'user:green' : u'/icons/images/user_green.png',
	u'user:male' : u'/icons/images/user_male.png',
	u'user:orange' : u'/icons/images/user_orange.png',
	u'user:red' : u'/icons/images/user_red.png',
	u'user:suit' : u'/icons/images/user_suit.png',
	u'warning' : u'/icons/images/warning.png',
	u'webcam' : u'/icons/images/webcam.png',
	u'yen' : u'/icons/images/yen.png',
	u'8ball' : u'/icons/images/8ball.png',
	u'accept' : u'/icons/images/accept.png',
	u'add' : u'/icons/images/add.png',
	u'asterisk' : u'/icons/images/asterisk_yellow.png',
	u'asterisk:orange' : u'/icons/images/asterisk_orange.png',
	u'asterisk:yellow' : u'/icons/images/asterisk_yellow.png',
	u'basketball' : u'/icons/images/basketball.png',
	u'book' : u'/icons/images/book_open.png',
	u'book:closed' : u'/icons/images/book_closed.png',
	u'book:open' : u'/icons/images/book_open.png',
	u'bug' : u'/icons/images/bug.png',
	u'bullet' : u'/icons/images/bullet_blue.png',
	u'building' : u'/icons/images/building.png',
	u'bullet:add' : u'/icons/images/bullet_add.png',
	u'bullet:black' : u'/icons/images/bullet_black.png',
	u'bullet:blue' : u'/icons/images/bullet_blue.png',
	u'bullet:delete' : u'/icons/images/bullet_delete.png',
	u'bullet:green' : u'/icons/images/bullet_green.png',
	u'bullet:orange' : u'/icons/images/bullet_orange.png',
	u'bullet:pink' : u'/icons/images/bullet_pink.png',
	u'bullet:purple' : u'/icons/images/bullet_purple.png',
	u'bullet:red' : u'/icons/images/bullet_red.png',
	u'bullet:star' : u'/icons/images/bullet_star.png',
	u'bullet:yellow' : u'/icons/images/bullet_yellow.png',
	u'cake' : u'/icons/images/cake.png',
	u'calculator' : u'/icons/images/calculator.png',
	u'calendar' : u'/icons/images/calendar.png',
	u'camera' : u'/icons/images/camera.png',
	u'cancel' : u'/icons/images/cancel.png',
	u'car' : u'/icons/images/car.png',
	u'cd' : u'/icons/images/cd.png',
	u'cell' : u'/icons/images/cell.png',
	u'chart' : u'/icons/images/chart_bar.png',
	u'chart:bar' : u'/icons/images/chart_bar.png',
	u'chart:graphic' : u'/icons/images/chart_graphic.png',
	u'chart:pie' : u'/icons/images/chart_pie.png',
	u'clock' : u'/icons/images/clock_blue.png',
	u'clock:blue' : u'/icons/images/clock_blue.png',
	u'clock:red' : u'/icons/images/clock_red.png',
	u'coffe' : u'/icons/images/coffe.png',
	u'cog' : u'/icons/images/cog.png',
	u'coins' : u'/icons/images/coins.png',
	u'comment' : u'/icons/images/comment.png',
	u'comments' : u'/icons/images/comments.png',
	u'computer' : u'/icons/images/computer.png',
	u'cross' : u'/icons/images/cross.png',
	u'database' : u'/icons/images/database.png',
	u'date' : u'/icons/images/date.png',
	u'delete' : u'/icons/images/delete.png',
	u'disk' : u'/icons/images/disk.png',
	u'dollar' : u'/icons/images/dollar.png',
	u'drink' : u'/icons/images/drink.png',
	u'drive' : u'/icons/images/drive_cd.png',
	u'drive:cd' : u'/icons/images/drive_cd.png',
	u'drive:network' : u'/icons/images/drive_network.png',
	u'dvd' : u'/icons/images/dvd.png',
	u'error' : u'/icons/images/error.png',
	u'euro' : u'/icons/images/euro.png',
	u'eye' : u'/icons/images/eye.png',
	u'film' : u'/icons/images/film.png',
	u'flag' : u'/icons/images/flag_red.png',
	u'flag:blue' : u'/icons/images/flag_blue.png',
	u'flag:green' : u'/icons/images/flag_green.png',
	u'flag:orange' : u'/icons/images/flag_orange.png',
	u'flag:pink' : u'/icons/images/flag_pink.png',
	u'flag:purple' : u'/icons/images/flag_purple.png',
	u'flag:red' : u'/icons/images/flag_red.png',
	u'flag:yellow' : u'/icons/images/flag_yellow.png',
	u'folder' : u'/icons/images/folder.png',
	u'football' : u'/icons/images/football.png',
	u'golf' : u'/icons/images/golf.png',
	u'heart' : u'/icons/images/heart.png',
	u'hourglass' : u'/icons/images/hourglass.png',
	u'information' : u'/icons/images/information.png',
	u'ipod' : u'/icons/images/ipod.png',
	u'key' : u'/icons/images/key.png',
	u'keyboard' : u'/icons/images/keyboard.png',
	u'layers' : u'/icons/images/layers.png',
	u'lego' : u'/icons/images/lego.png',
	u'lightbulb' : u'/icons/images/lightbulb_on.png',
	u'lightbulb:off' : u'/icons/images/lightbulb_off.png',
	u'lightbulb:on' : u'/icons/images/lightbulb_on.png',
	u'lightning' : u'/icons/images/lightning.png',
	u'lock' : u'/icons/images/lock.png',
	u'male' : u'/icons/images/male.png',
	u'medal' : u'/icons/images/medal_gold_blue.png',
	u'medal:bronze' : u'/icons/images/medal_bronze_blue.png',
	u'medal:bronze:blue' : u'/icons/images/medal_bronze_blue.png',
	u'medal:bronze:green' : u'/icons/images/medal_bronze_green.png',
	u'medal:bronze:red' : u'/icons/images/medal_bronze_red.png',
	u'medal:gold' : u'/icons/images/medal_gold_blue.png',
	u'medal:gold:blue' : u'/icons/images/medal_gold_blue.png',
	u'medal:gold:green' : u'/icons/images/medal_gold_green.png',
	u'medal:gold:red' : u'/icons/images/medal_gold_red.png',
	u'medal:silver' : u'/icons/images/medal_silver_blue.png',
	u'medal:silver:blue' : u'/icons/images/medal_silver_blue.png',
	u'medal:silver:green' : u'/icons/images/medal_silver_green.png',
	u'medal:silver:red' : u'/icons/images/medal_silver_red.png',
	u'medal:star' : u'/icons/images/medal_star_gold_blue.png',
	u'medal:star:bronze' : u'/icons/images/medal_star_bronze_blue.png',
	u'medal:star:bronze:blue' : u'/icons/images/medal_star_bronze_blue.png',
	u'medal:star:bronze:green' : u'/icons/images/medal_star_bronze_green.png',
	u'medal:star:bronze:red' : u'/icons/images/medal_star_bronze_red.png',
	u'medal:star:gold' : u'/icons/images/medal_star_gold_blue.png',
	u'medal:star:gold:blue' : u'/icons/images/medal_star_gold_blue.png',
	u'medal:star:gold:green' : u'/icons/images/medal_star_gold_green.png',
	u'medal:star:gold:red' : u'/icons/images/medal_star_gold_red.png',
	u'medal:star:silver' : u'/icons/images/medal_star_silver_blue.png',
	u'medal:star:silver:blue' : u'/icons/images/medal_star_silver_blue.png',
	u'medal:star:silver:green' : u'/icons/images/medal_star_silver_green.png',
	u'medal:star:silver:red' : u'/icons/images/medal_star_silver_red.png',
	u'scissors' : u'/icons/images/scissors.png'
	})