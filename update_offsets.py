#!/usr/bin/env python3
"""
RBX External - Automatic Offset Updater
Fetches latest offsets from rbxoffsets.xyz API
"""

import requests
import re
import sys
from pathlib import Path

API_BASE    = "https://rbxoffsets.xyz"
HEADERS     = {"rbxoffsets.xyz": "apiv1"}
OFFSET_FILE = Path("src/engine/offset.h")


def get_latest_version():
    try:
        r = requests.get(f"{API_BASE}/api/version/raw", headers=HEADERS, timeout=10)
        return r.text.strip() if r.status_code == 200 else None
    except Exception as e:
        print(f"[-] Error fetching version: {e}")
        return None


def get_latest_offsets():
    try:
        r = requests.get(f"{API_BASE}/api/latest/raw", headers=HEADERS, timeout=10)
        return r.text if r.status_code == 200 else None
    except Exception as e:
        print(f"[-] Error fetching offsets: {e}")
        return None


def get_current_version():
    try:
        content = OFFSET_FILE.read_text(encoding="utf-8")
        m = re.search(r'ClientVersion\s*=\s*"([^"]+)"', content)
        return m.group(1) if m else None
    except Exception as e:
        print(f"[-] Error reading current version: {e}")
        return None


def get_compat_shims():
    """Compatibility namespace shims — maps old nested namespaces to the new flat layout."""
    return r"""
// ─── Compatibility shims ─────────────────────────────────────────────────────
namespace fakemodel {
    static constexpr uintptr_t Pointer       = offsets::FakeDataModelPointer;
    static constexpr uintptr_t RealDataModel = offsets::FakeDataModelToDataModel;
}
namespace render {
    static constexpr uintptr_t Pointer    = offsets::VisualEnginePointer;
    static constexpr uintptr_t Dimensions = offsets::Dimensions;
    static constexpr uintptr_t ViewMatrix = offsets::viewmatrix;
}
namespace view {
    static constexpr uintptr_t DeviceD3D11   = offsets::DeviceD3D11;
    static constexpr uintptr_t LightingValid = offsets::LightingValid;
    static constexpr uintptr_t SkyValid      = offsets::SkyValid;
    static constexpr uintptr_t render        = offsets::VisualEngine;
}
namespace camera {
    static constexpr uintptr_t Position        = offsets::CameraPos;
    static constexpr uintptr_t Rotation        = offsets::CameraRotation;
    static constexpr uintptr_t FieldOfView     = offsets::FOV;
    static constexpr uintptr_t Viewport        = offsets::CameraViewport;
    static constexpr uintptr_t ViewportSize    = offsets::ViewportSize;
    static constexpr uintptr_t CameraSubject   = offsets::CameraSubject;
    static constexpr uintptr_t CameraType      = offsets::CameraType;
    static constexpr uintptr_t ImagePlaneDepth = offsets::CameraImagePlaneDepth;
}
namespace player {
    static constexpr uintptr_t UserId        = offsets::UserId;
    static constexpr uintptr_t LocalPlayer   = offsets::LocalPlayer;
    static constexpr uintptr_t ModelInstance = offsets::ModelInstance;
    static constexpr uintptr_t DisplayName   = offsets::DisplayName;
    static constexpr uintptr_t team          = offsets::Team;
    static constexpr uintptr_t TeamColor     = offsets::TeamColor;
    static constexpr uintptr_t CameraMode    = offsets::CameraMode;
    static constexpr uintptr_t mouse         = offsets::PlayerMouse;
    static constexpr uintptr_t AccountAge    = offsets::AccountAge;
    static constexpr uintptr_t LocaleId      = offsets::LocaleId;
}
namespace humanoid {
    static constexpr uintptr_t Health           = offsets::Health;
    static constexpr uintptr_t MaxHealth        = offsets::MaxHealth;
    static constexpr uintptr_t walkspeed        = offsets::WalkSpeed;
    static constexpr uintptr_t WalkspeedCheck   = offsets::WalkSpeedCheck;
    static constexpr uintptr_t RigType          = offsets::RigType;
    static constexpr uintptr_t PlatformStand    = offsets::PlatformStand;
    static constexpr uintptr_t HumanoidRootPart = offsets::HumanoidRootPartRef;
    static constexpr uintptr_t HumanoidState    = offsets::HumanoidState;
    static constexpr uintptr_t HumanoidStateID  = offsets::HumanoidStateId;
    static constexpr uintptr_t Jump             = offsets::Jump;
    static constexpr uintptr_t JumpPower        = offsets::JumpPower;
    static constexpr uintptr_t JumpHeight       = offsets::JumpHeight;
    static constexpr uintptr_t HipHeight        = offsets::HipHeight;
    static constexpr uintptr_t AutoJumpEnabled  = offsets::AutoJumpEnabled;
    static constexpr uintptr_t SeatPart         = offsets::SeatPart;
    static constexpr uintptr_t CameraOffset     = offsets::CameraOffset;
    static constexpr uintptr_t IsWalking        = offsets::IsWalking;
}
namespace primitive {
    static constexpr uintptr_t Position                = offsets::Position;
    static constexpr uintptr_t Rotation                = offsets::CFrame;
    static constexpr uintptr_t Size                    = offsets::PartSize;
    static constexpr uintptr_t AssemblyLinearVelocity  = offsets::PrimitiveAssemblyLinearVelocity;
    static constexpr uintptr_t AssemblyAngularVelocity = offsets::PrimitiveAssemblyAngularVelocity;
    static constexpr uintptr_t Owner                   = offsets::PrimitiveOwner;
    static constexpr uintptr_t Flags                   = offsets::PrimitiveFlags;
    static constexpr uintptr_t Material                = offsets::MaterialType;
    static constexpr uintptr_t Validate                = offsets::ValidatePrimitive;
}
namespace primitiveflag {
    static constexpr uintptr_t Anchored   = offsets::Anchored;
    static constexpr uintptr_t CanCollide = offsets::CanCollide;
    static constexpr uintptr_t CanQuery   = offsets::CanQuery;
    static constexpr uintptr_t CanTouch   = offsets::CanTouch;
}
namespace basepart {
    static constexpr uintptr_t primitive    = offsets::Primitive;
    static constexpr uintptr_t Transparency = offsets::Transparency;
    static constexpr uintptr_t Color3       = offsets::Color3;
    static constexpr uintptr_t CastShadow   = offsets::BasePartCastShadow;
    static constexpr uintptr_t Locked       = offsets::BasePartLocked;
    static constexpr uintptr_t Massless     = offsets::BasePartMassless;
    static constexpr uintptr_t Reflectance  = offsets::BasePartReflectance;
    static constexpr uintptr_t Shape        = offsets::Shape;
}
namespace meshpart {
    static constexpr uintptr_t MeshId  = offsets::MeshId;
    static constexpr uintptr_t Texture = offsets::MeshPartTexture;
}
namespace instance {
    static constexpr uintptr_t name            = offsets::Name;
    static constexpr uintptr_t parent          = offsets::Parent;
    static constexpr uintptr_t ChildrenStart   = offsets::Children;
    static constexpr uintptr_t ChildrenEnd     = offsets::ChildrenEnd;
    static constexpr uintptr_t ClassDescriptor = offsets::ClassDescriptor;
    static constexpr uintptr_t ClassBase       = offsets::ClassBase;
    static constexpr uintptr_t This            = offsets::This;
}
namespace gui {
    static constexpr uintptr_t Size                   = offsets::GuiSize;
    static constexpr uintptr_t Position               = offsets::GuiPosition;
    static constexpr uintptr_t text                   = offsets::TextLabelText;
    static constexpr uintptr_t Visible                = offsets::TextLabelVisible;
    static constexpr uintptr_t ZIndex                 = offsets::ZIndex;
    static constexpr uintptr_t LayoutOrder            = offsets::LayoutOrder;
    static constexpr uintptr_t RichText               = offsets::RichText;
    static constexpr uintptr_t Image                  = offsets::Image;
    static constexpr uintptr_t TextColor3             = offsets::TextColor3;
    static constexpr uintptr_t ScreenGui_Enabled      = offsets::ScreenGui_Enabled;
    static constexpr uintptr_t BackgroundColor3       = offsets::BackgroundColor3;
    static constexpr uintptr_t BackgroundTransparency = offsets::BackgroundTransparency;
}
namespace datamodel {
    static constexpr uintptr_t PlaceId        = offsets::PlaceId;
    static constexpr uintptr_t GameId         = offsets::GameId;
    static constexpr uintptr_t CreatorId      = offsets::CreatorId;
    static constexpr uintptr_t ServerIP       = offsets::ServerIP;
    static constexpr uintptr_t workspace      = offsets::Workspace;
    static constexpr uintptr_t scriptcontext  = offsets::ScriptContext;
    static constexpr uintptr_t GameLoaded     = offsets::GameLoaded;
    static constexpr uintptr_t JobId          = offsets::JobId;
    static constexpr uintptr_t PlaceVersion   = offsets::PlaceVersion;
    static constexpr uintptr_t PrimitiveCount = offsets::DataModelPrimitiveCount;
    static constexpr uintptr_t ToRenderView1  = offsets::DataModelToRenderView1;
    static constexpr uintptr_t ToRenderView2  = offsets::DataModelToRenderView2;
    static constexpr uintptr_t ToRenderView3  = offsets::DataModelToRenderView3;
}
namespace workspace { static constexpr uintptr_t world = offsets::World; }
namespace world {
    static constexpr uintptr_t Gravity         = offsets::Gravity;
    static constexpr uintptr_t ReadOnlyGravity  = offsets::ReadOnlyGravity;
}
namespace light {
    static constexpr uintptr_t Ambient               = offsets::LightingAmbient;
    static constexpr uintptr_t OutdoorAmbient        = offsets::OutdoorAmbient;
    static constexpr uintptr_t Brightness            = offsets::LightingBrightness;
    static constexpr uintptr_t ClockTime             = offsets::ClockTime;
    static constexpr uintptr_t LightColor            = offsets::LightColor;
    static constexpr uintptr_t LightDirection        = offsets::LightDirection;
    static constexpr uintptr_t SunPosition           = offsets::SunPosition;
    static constexpr uintptr_t MoonPosition          = offsets::MoonPosition;
    static constexpr uintptr_t FogEnd                = offsets::FogEnd;
    static constexpr uintptr_t FogStart              = offsets::FogStart;
    static constexpr uintptr_t FogColor              = offsets::FogColor;
    static constexpr uintptr_t ExposureCompensation  = offsets::ExposureCompensation;
    static constexpr uintptr_t GlobalShadows         = offsets::GlobalShadows;
    static constexpr uintptr_t ColorShift_Top        = offsets::ColorShift_Top;
    static constexpr uintptr_t ColorShift_Bottom     = offsets::ColorShift_Bottom;
    static constexpr uintptr_t GeographicLatitude    = offsets::GeographicLatitude;
    static constexpr uintptr_t EnvironmentDiffuseScale  = offsets::EnvironmentDiffuseScale;
    static constexpr uintptr_t EnvironmentSpecularScale = offsets::EnvironmentSpecularScale;
    static constexpr uintptr_t sky                   = offsets::Sky;
}
namespace mouseservice {
    static constexpr uintptr_t InputObject        = offsets::InputObject;
    static constexpr uintptr_t InputObject2       = offsets::InputObject;
    static constexpr uintptr_t MousePosition      = offsets::MousePosition;
    static constexpr uintptr_t SensitivityPointer = offsets::MouseSensitivity;
}
namespace misc {
    static constexpr uintptr_t Value        = offsets::Value;
    static constexpr uintptr_t AnimationId  = offsets::AnimationId;
    static constexpr uintptr_t StringLength = offsets::StringLength;
    static constexpr uintptr_t Adornee      = offsets::Adornee;
}
namespace silent {
    static constexpr uintptr_t FramePositionOffsetX = 0x0;
    static constexpr uintptr_t FramePositionOffsetY = 0x8;
}
namespace animation {
    static constexpr uintptr_t animator     = 0x100;
    static constexpr uintptr_t IsPlaying    = 0xa40;
    static constexpr uintptr_t Looped       = 0xdd;
    static constexpr uintptr_t Speed        = 0xcc;
    static constexpr uintptr_t TimePosition = 0xd0;
    static constexpr uintptr_t AnimationId  = offsets::AnimationId;
}
namespace animator { static constexpr uintptr_t ActiveAnimations = offsets::ActiveAnimations; }
namespace task {
    static constexpr uintptr_t Pointer  = offsets::TaskSchedulerPointer;
    static constexpr uintptr_t JobStart = offsets::JobStart;
    static constexpr uintptr_t JobEnd   = offsets::JobEnd;
    static constexpr uintptr_t JobName  = offsets::Job_Name;
    static constexpr uintptr_t MaxFPS   = offsets::TaskSchedulerMaxFPS;
}
namespace run {
    static constexpr uintptr_t HeartbeatFPS  = offsets::HeartbeatFPS;
    static constexpr uintptr_t HeartbeatTask = offsets::HeartbeatTask;
}
namespace physics_sender {
    static constexpr uintptr_t MaxBandwidthBps = offsets::PhysicsSenderMaxBandwidthBps;
}
namespace job {
    static constexpr uintptr_t fakemodel     = offsets::RenderJobFakeDataModel;
    static constexpr uintptr_t RealDataModel = offsets::RenderJobRealDataModel;
    static constexpr uintptr_t view          = offsets::RenderJobRenderView;
}
namespace prompt {
    static constexpr uintptr_t ActionText           = offsets::ProximityPromptActionText;
    static constexpr uintptr_t Enabled              = offsets::ProximityPromptEnabled;
    static constexpr uintptr_t GamepadKeyCode        = offsets::ProximityPromptGamepadKeyCode;
    static constexpr uintptr_t HoldDuration          = offsets::ProximityPromptHoldDuraction;
    static constexpr uintptr_t MaxActivationDistance = offsets::ProximityPromptMaxActivationDistance;
    static constexpr uintptr_t KeyCode               = offsets::KeyCode;
    static constexpr uintptr_t RequiresLineOfSight   = offsets::RequiresLineOfSight;
    static constexpr uintptr_t ObjectText            = offsets::ProximityPromptMaxObjectText;
}
"""


def update_offset_file(content, version):
    """Write new offset.h with header + flat offsets + compat shims."""
    try:
        lines = [
            "#pragma once",
            "",
            "#include <cstdint>",
            "#include <string>",
            "namespace offset {",
            f'    inline std::string ClientVersion = "{version}";',
            "",
            content.strip(),
            "",
            get_compat_shims(),
            "",
            "} // end namespace offset",
            "",
        ]
        OFFSET_FILE.write_text('\n'.join(lines), encoding="utf-8")
        return True
    except Exception as e:
        print(f"[-] Error writing offset file: {e}")
        return False


def main():
    print("=" * 50)
    print("   RBX External - Offset Updater")
    print("=" * 50)
    print()

    current = get_current_version()
    if not current:
        print("[-] Could not read current version from offset.h")
        return 1
    print(f"[*] Current version : {current}")
    print(f"[*] Checking for updates...")

    latest = get_latest_version()
    if not latest:
        print("[-] Failed to fetch latest version from API")
        return 1
    print(f"[*] Latest version  : {latest}")

    if latest == current:
        print("[+] Offsets are already up to date!")
        return 0

    print(f"[!] Update available: {current} -> {latest}")
    print(f"[*] Downloading latest offsets...")

    content = get_latest_offsets()
    if not content:
        print("[-] Failed to fetch latest offsets from API")
        return 1

    print(f"[*] Writing offset.h...")
    if not update_offset_file(content, latest):
        print("[-] Failed to write offset file")
        return 1

    print(f"[+] Successfully updated: {current} -> {latest}")
    print()
    print("[!] Rebuild the project to apply:")
    print("    msbuild rbx-external.sln /p:Configuration=Release /p:Platform=x64")
    return 0


if __name__ == "__main__":
    sys.exit(main())
