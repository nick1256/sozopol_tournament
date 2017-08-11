# update scren size
def go_to_window(sm,window_name):	
	
	# change current screen	
	sm.current = window_name
	print(sm.current)
	# adjust size of window
	Window.size = screens[window_name].window_size

