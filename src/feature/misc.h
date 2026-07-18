#pragma once
#include <vector>
#include <string>

namespace misc {
    void fly();
    void walkspeed();
    void hitbox();
    void desync();
    void tickrate();
    void anim_changer();
    void lighting();
    void bhop();
    void noclip();
    void freeze_players();
    void run();

    const char** anim_pack_names(int* count_out);
}

namespace console {
    void render();
    bool is_open();
    void toggle();
}
