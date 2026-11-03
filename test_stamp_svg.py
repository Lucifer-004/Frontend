def get_3d_stamp_svg(color='green', size=48):
    is_green = (color.lower() == 'green')
    grad_id = 'stampGradGreen' if is_green else 'stampGradBlue'
    core_id = 'stampCoreGreen' if is_green else 'stampCoreBlue'
    star_id = 'stampGoldStar'
    
    c_start = '#145a32' if is_green else '#154360'
    c_mid   = '#2ecc71' if is_green else '#3498db'
    c_light = '#abebc6' if is_green else '#aed6f1'
    
    path_d = 'M 57.00 30.00 Q 53.54 34.68 54.94 40.33 Q 49.96 43.33 49.09 49.09 Q 43.33 49.96 40.33 54.94 Q 34.68 53.54 30.00 57.00 Q 25.32 53.54 19.67 54.94 Q 16.67 49.96 10.91 49.09 Q 10.04 43.33 5.06 40.33 Q 6.46 34.68 3.00 30.00 Q 6.46 25.32 5.06 19.67 Q 10.04 16.67 10.91 10.91 Q 16.67 10.04 19.67 5.06 Q 25.32 6.46 30.00 3.00 Q 34.68 6.46 40.33 5.06 Q 43.33 10.04 49.09 10.91 Q 49.96 16.67 54.94 19.67 Q 53.54 25.32 57.00 30.00 Z'
    
    emblem = '''<polygon points="30,18 33,25 41,25 35,29 37,37 30,32 23,37 25,29 19,25 27,25" fill="url(#''' + star_id + ''')" stroke="#996e14" stroke-width="0.5"/>''' if is_green else '''<polygon points="30,16 35,25 43,30 35,35 30,44 25,35 17,30 25,25" fill="url(#''' + star_id + ''')" stroke="#996e14" stroke-width="0.5"/>'''
    
    svg = f'''<svg class="stamp-3d-svg" viewBox="0 0 60 60" width="{size}" height="{size}" style="filter:drop-shadow(0 4px 10px {'rgba(46,204,113,0.5)' if is_green else 'rgba(52,152,219,0.5)'})">
  <defs>
    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c_start}"/>
      <stop offset="45%" stop-color="{c_mid}"/>
      <stop offset="70%" stop-color="{c_light}"/>
      <stop offset="100%" stop-color="{c_start}"/>
    </linearGradient>
    <radialGradient id="{core_id}" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="{c_light}"/>
      <stop offset="50%" stop-color="{c_mid}"/>
      <stop offset="100%" stop-color="{c_start}"/>
    </radialGradient>
    <linearGradient id="{star_id}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff5cc"/>
      <stop offset="50%" stop-color="#f1c40f"/>
      <stop offset="100%" stop-color="#b7950b"/>
    </linearGradient>
  </defs>
  <!-- Scalloped rim -->
  <path d="{path_d}" fill="url(#{grad_id})" stroke="rgba(255,255,255,0.4)" stroke-width="1"/>
  <!-- Perforated / Stitched ring -->
  <circle cx="30" cy="30" r="21.5" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="1.2" stroke-dasharray="2.5 2"/>
  <!-- Embossed core -->
  <circle cx="30" cy="30" r="17" fill="url(#{core_id})" stroke="rgba(0,0,0,0.35)" stroke-width="1"/>
  <!-- Raised emblem -->
  {emblem}
  <!-- Specular highlight -->
  <path d="M 18,22 C 22,14 38,14 42,22 C 37,17 23,17 18,22 Z" fill="rgba(255,255,255,0.45)"/>
</svg>'''
    return svg

print("Length of green SVG:", len(get_3d_stamp_svg('green', 48)))
print("Length of blue SVG:", len(get_3d_stamp_svg('blue', 48)))

