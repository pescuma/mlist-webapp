#!/usr/bin/env python
# coding=utf-8

wikisyntax_images = dict({
	u'money' : u'/icons/images/money.gif',
	u'monitor' : u'/icons/images/monitor.gif',
	u'mouse' : u'/icons/images/mouse.gif',
	u'note' : u'/icons/images/note.gif',
	u'page' : u'/icons/images/page.gif',
	u'pill' : u'/icons/images/pill.gif',
	u'pound' : u'/icons/images/pound.gif',
	u'printer' : u'/icons/images/printer.gif',
	u'question' : u'/icons/images/question.gif',
	u'raquet' : u'/icons/images/raquet.gif',
	u'report' : u'/icons/images/report.gif',
	u'ruby' : u'/icons/images/ruby.gif',
	u'shield' : u'/icons/images/shield.gif',
	u'shuttlecock' : u'/icons/images/shuttlecock.gif',
	u'soccer' : u'/icons/images/soccer.gif',
	u'star' : u'/icons/images/star.gif',
	u'stop' : u'/icons/images/stop.gif',
	u'telephone' : u'/icons/images/telephone.gif',
	u'tennis' : u'/icons/images/tennis.gif',
	u'tick' : u'/icons/images/tick.gif',
	u'time' : u'/icons/images/time.gif',
	u'trash' : u'/icons/images/trash.gif',
	u'tree' : u'/icons/images/tree.gif',
	u'tv' : u'/icons/images/tv.gif',
	u'user' : u'/icons/images/user_male.gif',
	u'user:female' : u'/icons/images/user_female.gif',
	u'user:gray' : u'/icons/images/user_gray.gif',
	u'user:green' : u'/icons/images/user_green.gif',
	u'user:male' : u'/icons/images/user_male.gif',
	u'user:orange' : u'/icons/images/user_orange.gif',
	u'user:red' : u'/icons/images/user_red.gif',
	u'user:suit' : u'/icons/images/user_suit.gif',
	u'warning' : u'/icons/images/warning.gif',
	u'webcam' : u'/icons/images/webcam.gif',
	u'yen' : u'/icons/images/yen.gif',
	u'8ball' : u'/icons/images/8ball.gif',
	u'accept' : u'/icons/images/accept.gif',
	u'add' : u'/icons/images/add.gif',
	u'asterisk' : u'/icons/images/asterisk_yellow.gif',
	u'asterisk:orange' : u'/icons/images/asterisk_orange.gif',
	u'asterisk:yellow' : u'/icons/images/asterisk_yellow.gif',
	u'basketball' : u'/icons/images/basketball.gif',
	u'book' : u'/icons/images/book_open.gif',
	u'book:closed' : u'/icons/images/book_closed.gif',
	u'book:open' : u'/icons/images/book_open.gif',
	u'bug' : u'/icons/images/bug.gif',
	u'bullet' : u'/icons/images/bullet_blue.gif',
	u'building' : u'/icons/images/building.gif',
	u'bullet:add' : u'/icons/images/bullet_add.gif',
	u'bullet:black' : u'/icons/images/bullet_black.gif',
	u'bullet:blue' : u'/icons/images/bullet_blue.gif',
	u'bullet:delete' : u'/icons/images/bullet_delete.gif',
	u'bullet:green' : u'/icons/images/bullet_green.gif',
	u'bullet:orange' : u'/icons/images/bullet_orange.gif',
	u'bullet:pink' : u'/icons/images/bullet_pink.gif',
	u'bullet:purple' : u'/icons/images/bullet_purple.gif',
	u'bullet:red' : u'/icons/images/bullet_red.gif',
	u'bullet:star' : u'/icons/images/bullet_star.gif',
	u'bullet:yellow' : u'/icons/images/bullet_yellow.gif',
	u'cake' : u'/icons/images/cake.gif',
	u'calculator' : u'/icons/images/calculator.gif',
	u'calendar' : u'/icons/images/calendar.gif',
	u'camera' : u'/icons/images/camera.gif',
	u'cancel' : u'/icons/images/cancel.gif',
	u'car' : u'/icons/images/car.gif',
	u'cd' : u'/icons/images/cd.gif',
	u'cell' : u'/icons/images/cell.gif',
	u'chart' : u'/icons/images/chart_bar.gif',
	u'chart:bar' : u'/icons/images/chart_bar.gif',
	u'chart:graphic' : u'/icons/images/chart_graphic.gif',
	u'chart:pie' : u'/icons/images/chart_pie.gif',
	u'clock' : u'/icons/images/clock_blue.gif',
	u'clock:blue' : u'/icons/images/clock_blue.gif',
	u'clock:red' : u'/icons/images/clock_red.gif',
	u'coffe' : u'/icons/images/coffe.gif',
	u'cog' : u'/icons/images/cog.gif',
	u'coins' : u'/icons/images/coins.gif',
	u'comment' : u'/icons/images/comment.gif',
	u'comments' : u'/icons/images/comments.gif',
	u'computer' : u'/icons/images/computer.gif',
	u'cross' : u'/icons/images/cross.gif',
	u'database' : u'/icons/images/database.gif',
	u'date' : u'/icons/images/date.gif',
	u'delete' : u'/icons/images/delete.gif',
	u'disk' : u'/icons/images/disk.gif',
	u'dollar' : u'/icons/images/dollar.gif',
	u'drink' : u'/icons/images/drink.gif',
	u'drive' : u'/icons/images/drive_cd.gif',
	u'drive:cd' : u'/icons/images/drive_cd.gif',
	u'drive:network' : u'/icons/images/drive_network.gif',
	u'dvd' : u'/icons/images/dvd.gif',
	u'error' : u'/icons/images/error.gif',
	u'euro' : u'/icons/images/euro.gif',
	u'eye' : u'/icons/images/eye.gif',
	u'female' : u'/icons/images/female.gif',
	u'film' : u'/icons/images/film.gif',
	u'flag' : u'/icons/images/flag_red.gif',
	u'flag:blue' : u'/icons/images/flag_blue.gif',
	u'flag:green' : u'/icons/images/flag_green.gif',
	u'flag:orange' : u'/icons/images/flag_orange.gif',
	u'flag:pink' : u'/icons/images/flag_pink.gif',
	u'flag:purple' : u'/icons/images/flag_purple.gif',
	u'flag:red' : u'/icons/images/flag_red.gif',
	u'flag:yellow' : u'/icons/images/flag_yellow.gif',
	u'folder' : u'/icons/images/folder.gif',
	u'football' : u'/icons/images/football.gif',
	u'golf' : u'/icons/images/golf.gif',
	u'heart' : u'/icons/images/heart.gif',
	u'hourglass' : u'/icons/images/hourglass.gif',
	u'information' : u'/icons/images/information.gif',
	u'ipod' : u'/icons/images/ipod.gif',
	u'key' : u'/icons/images/key.gif',
	u'keyboard' : u'/icons/images/keyboard.gif',
	u'layers' : u'/icons/images/layers.gif',
	u'lego' : u'/icons/images/lego.gif',
	u'lightbulb' : u'/icons/images/lightbulb_on.gif',
	u'lightbulb:off' : u'/icons/images/lightbulb_off.gif',
	u'lightbulb:on' : u'/icons/images/lightbulb_on.gif',
	u'lightning' : u'/icons/images/lightning.gif',
	u'lock' : u'/icons/images/lock.gif',
	u'male' : u'/icons/images/male.gif',
	u'medal' : u'/icons/images/medal_gold_blue.gif',
	u'medal:bronze' : u'/icons/images/medal_bronze_blue.gif',
	u'medal:bronze:blue' : u'/icons/images/medal_bronze_blue.gif',
	u'medal:bronze:green' : u'/icons/images/medal_bronze_green.gif',
	u'medal:bronze:red' : u'/icons/images/medal_bronze_red.gif',
	u'medal:gold' : u'/icons/images/medal_gold_blue.gif',
	u'medal:gold:blue' : u'/icons/images/medal_gold_blue.gif',
	u'medal:gold:green' : u'/icons/images/medal_gold_green.gif',
	u'medal:gold:red' : u'/icons/images/medal_gold_red.gif',
	u'medal:silver' : u'/icons/images/medal_silver_blue.gif',
	u'medal:silver:blue' : u'/icons/images/medal_silver_blue.gif',
	u'medal:silver:green' : u'/icons/images/medal_silver_green.gif',
	u'medal:silver:red' : u'/icons/images/medal_silver_red.gif',
	u'medal:star' : u'/icons/images/medal_star_gold_blue.gif',
	u'medal:star:bronze' : u'/icons/images/medal_star_bronze_blue.gif',
	u'medal:star:bronze:blue' : u'/icons/images/medal_star_bronze_blue.gif',
	u'medal:star:bronze:green' : u'/icons/images/medal_star_bronze_green.gif',
	u'medal:star:bronze:red' : u'/icons/images/medal_star_bronze_red.gif',
	u'medal:star:gold' : u'/icons/images/medal_star_gold_blue.gif',
	u'medal:star:gold:blue' : u'/icons/images/medal_star_gold_blue.gif',
	u'medal:star:gold:green' : u'/icons/images/medal_star_gold_green.gif',
	u'medal:star:gold:red' : u'/icons/images/medal_star_gold_red.gif',
	u'medal:star:silver' : u'/icons/images/medal_star_silver_blue.gif',
	u'medal:star:silver:blue' : u'/icons/images/medal_star_silver_blue.gif',
	u'medal:star:silver:green' : u'/icons/images/medal_star_silver_green.gif',
	u'medal:star:silver:red' : u'/icons/images/medal_star_silver_red.gif',
	u'scissors' : u'/icons/images/scissors.gif'
	})