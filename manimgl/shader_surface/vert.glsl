#version 330
in vec3 point;
in vec3 du_point;
in vec3 dv_point;
in vec4 rgba;
out vec4 v_color;
#INSERT emit_gl_Position.glsl
#INSERT get_unit_normal.glsl

uniform vec3 camera_position;
uniform float time;
uniform float brightness = 1.5;

vec3 pal(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
    return a + b * cos(6.28318 * (c * t + d));
}

vec3 spectrum(float t) {
    return pal(t,
        vec3(0.5),
        vec3(0.5),
        vec3(1.0),
        vec3(0.0, 0.33, 0.67)
    );
}

vec4 finalize_color(vec4 color, vec3 point, vec3 unit_normal){
    vec3 n = normalize(unit_normal);
    vec3 to_camera = normalize(camera_position - point);

    // === 玻璃发光核心效果 ===

    // 1. 边缘发光效果 (Fresnel-like glow)
    float fresnel = 1.0 - abs(dot(n, to_camera));
    fresnel = pow(fresnel, 2.0); // 强化边缘

    // 2. 体积感的内部发光
    float inner_glow = 0.3 + 0.7 * sin(time * 2.0 + length(point) * 3.0);
    inner_glow *= 0.4; // 控制强度

    // 3. 动态颜色波动 - 模拟4D几何的色彩变化
    float wave1 = sin(dot(point.xy, vec2(2.0, 3.0)) + time * 1.5);
    float wave2 = cos(dot(point.yz, vec2(1.5, 2.5)) + time * 2.0);
    float wave3 = sin(length(point.xz) * 2.0 - time * 2.5);

    float color_shift = (wave1 + wave2 + wave3) * 0.2;
    float t = fresnel + color_shift + inner_glow;

    // 4. 使用spectrum调色板 - 蓝绿紫色调
    vec3 base_color = spectrum(t * 0.8 + 0.2);

    // 5. 添加特定的蓝绿色调 (模拟原始效果)
    vec3 tint = vec3(1.4, 2.1, 1.7); // 蓝绿色调
    base_color *= tint * 0.7;

    // 6. 紫色环境光 (模拟体积渲染的紫色辉光)
    vec3 purple_glow = vec3(0.6, 0.25, 0.7) * 0.3;
    base_color += purple_glow * (0.5 + 0.5 * sin(time + length(point)));

    // 7. 强烈的边缘高光
    float edge_highlight = pow(fresnel, 0.5) * 2.0;
    base_color += vec3(0.8, 1.0, 1.2) * edge_highlight * 0.4;

    // 8. 深度雾化效果
    float depth = length(point - camera_position);
    float fog_factor = smoothstep(2.0, 8.0, depth);
    vec3 fog_color = vec3(0.1, 0.2, 0.4);
    base_color = mix(base_color, fog_color, fog_factor * 0.3);

    // 9. 距离衰减 (模拟体积渲染的衰减)
    float distance_fade = 1.0 / (1.0 + depth * 0.1);
    base_color *= distance_fade;

    // 10. 动态亮度脉冲
    float pulse = 0.8 + 0.4 * sin(time * 3.0 + dot(point, vec3(1.0, 1.3, 0.7)));
    base_color *= pulse;

    // 11. 最终色彩强化和对比度调整
    base_color = pow(base_color, vec3(0.8)) * 1.5; // 提升亮度
    base_color = pow(base_color, vec3(1.2)); // 增加对比度

    // 12. 透明度效果 - 让材质看起来半透明
    float alpha = 0.7 + 0.3 * fresnel;
    base_color *= brightness;
    return vec4(base_color, alpha);
}

const float EPSILON = 1e-10;

void main() {
    // 设置顶点位置
    emit_gl_Position(point);

    // 计算导数向量
    vec3 du = du_point - point;
    vec3 dv = dv_point - point;

    // 计算法向量
    vec3 normal = cross(du, dv);
    float normal_mag = length(normal);

    // 单位法向量，处理法向量为零的情况
    vec3 unit_normal = (normal_mag < EPSILON) ?
        vec3(0.0, 0.0, sign(point.z)) : normalize(normal);

    // 计算最终颜色
    v_color = finalize_color(rgba, point, unit_normal);
}