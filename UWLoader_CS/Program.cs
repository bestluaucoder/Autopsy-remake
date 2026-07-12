using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace UWLoader
{
    static class Program
    {
        [DllImport("user32.dll")]
        private static extern bool SetProcessDPIAware();

        [STAThread]
        static void Main()
        {
            SetProcessDPIAware();
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }

    // ── Main loader form — neverlose layout ───────────────────────────────────
    public class MainForm : Form
    {
        // Win32 drag helpers
        public const int WM_NCLBUTTONDOWN = 0xA1;
        public const int HT_CAPTION = 0x2;
        [DllImport("user32.dll")] public static extern int SendMessage(IntPtr hWnd, int Msg, int wParam, int lParam);
        [DllImport("user32.dll")] public static extern bool ReleaseCapture();

        Button    _btnLoad;
        Label     _lblStatus;
        Timer     _debugTimer;
        Timer     _pollTimer;
        bool      _robloxRunning;

        static Image LoadRes(string name)
        {
            var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream(name);
            return stream != null ? Image.FromStream(stream) : null;
        }

        public MainForm()
        {
            // ── Form setup — exact neverlose Form2 dimensions ─────────────────
            FormBorderStyle = FormBorderStyle.None;
            StartPosition   = FormStartPosition.CenterScreen;
            ClientSize      = new Size(563, 429);
            DoubleBuffered  = true;
            BackColor       = Color.Black;

            // Background image stretched (same as neverlose Form2)
            var bg = LoadRes("background.png");
            if (bg != null) {
                BackgroundImage       = bg;
                BackgroundImageLayout = ImageLayout.Stretch;
            }

            // ── Username label — top-left, styled like neverlose ─────────────
            var lblUser = new Label {
                Text      = "@n1kvz",
                Font      = new Font("Verdana", 9f, FontStyle.Bold),
                ForeColor = Color.FromArgb(163, 212, 31),
                BackColor = Color.Transparent,
                AutoSize  = true,
                Location  = new Point(14, 14)
            };

            // ── Status label — positioned like nl "You have subscription." ────
            _lblStatus = new Label {
                Text      = "Waiting for Roblox...",
                Font      = new Font("Verdana", 8.25f),
                ForeColor = SystemColors.ControlLight,
                BackColor = Color.Transparent,
                AutoSize  = true,
                Location  = new Point(206, 370)
            };

            // ── Load button — exact neverlose position (298,380) size (148,38) ─
            _btnLoad = new Button {
                Location              = new Point(298, 380),
                Size                  = new Size(148, 38),
                FlatStyle             = FlatStyle.Flat,
                Font                  = new Font("Verdana", 8.25f),
                ForeColor             = SystemColors.ControlLight,
                Text                  = "Load",
                UseVisualStyleBackColor = true,
                Cursor                = Cursors.Hand
            };
            _btnLoad.FlatAppearance.BorderSize = 0;

            // Apply button-bg image if available
            var btnBg = LoadRes("button-bg.png");
            if (btnBg != null) {
                _btnLoad.BackgroundImage       = btnBg;
                _btnLoad.BackgroundImageLayout = ImageLayout.Stretch;
            }

            _btnLoad.Click     += OnLoad;
            _btnLoad.MouseDown += (s, e) => _btnLoad.ForeColor = Color.FromArgb(146, 189, 68);
            _btnLoad.MouseUp   += (s, e) => _btnLoad.ForeColor = SystemColors.ControlLight;

            Controls.Add(lblUser);
            Controls.Add(_lblStatus);
            Controls.Add(_btnLoad);

            MouseDown += Form_MouseDown;

            // ── Anti-debug timer (neverlose pattern) ─────────────────────────
            _debugTimer = new Timer { Interval = 1000 };
            _debugTimer.Tick += (s, e) => AntiDebug();
            _debugTimer.Start();

            // ── Roblox poll timer ─────────────────────────────────────────────
            _pollTimer = new Timer { Interval = 800 };
            _pollTimer.Tick += (s, e) => {
                bool now = Process.GetProcessesByName("RobloxPlayerBeta").Length > 0;
                if (now != _robloxRunning) {
                    _robloxRunning = now;
                    _lblStatus.Text = now ? "Roblox detected — click Load" : "Waiting for Roblox...";
                }
            };
            _pollTimer.Start();

            // ── Discord gate on first show ────────────────────────────────────
            Shown += async (s, e) => await DiscordGate();
        }

        void Form_MouseDown(object sender, MouseEventArgs e)
        {
            if (e.Button == MouseButtons.Left) {
                ReleaseCapture();
                SendMessage(Handle, WM_NCLBUTTONDOWN, HT_CAPTION, 0);
            }
        }

        async Task DiscordGate()
        {
            // Open invite in browser
            Process.Start(new ProcessStartInfo("https://discord.gg/Bgy7uae9x") { UseShellExecute = true });

            await Task.Delay(400); // let browser open

            var result = MessageBox.Show(
                "You must join the UW External Discord server to use this software.\n\n" +
                "discord.gg/Bgy7uae9x\n\n" +
                "The invite has been opened in your browser.\n" +
                "Once you have joined, click OK to continue.",
                "UW External — Join Discord",
                MessageBoxButtons.OKCancel,
                MessageBoxIcon.Information,
                MessageBoxDefaultButton.Button1,
                MessageBoxOptions.DefaultDesktopOnly);

            if (result != DialogResult.OK) Application.Exit();
        }

        async void OnLoad(object sender, EventArgs e)
        {
            _btnLoad.Enabled = false;
            _btnLoad.Text    = "Loading...";
            _lblStatus.Text  = "Extracting...";

            try {
                // Extract embedded rbx-external.exe
                string dir     = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "UWLoader");
                Directory.CreateDirectory(dir);
                string exePath = Path.Combine(dir, "rbx-external.exe");

                using (var stream = Assembly.GetExecutingAssembly()
                    .GetManifestResourceStream("rbx_external.exe"))
                {
                    if (stream == null) {
                        MessageBox.Show("Embedded exe missing. Rebuild after building rbx-external.",
                            "UW External", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                    using (var fs = File.Create(exePath))
                        stream.CopyTo(fs);
                }

                // Wait for Roblox (up to 120s)
                _lblStatus.Text = "Waiting for Roblox...";
                int waited = 0;
                while (Process.GetProcessesByName("RobloxPlayerBeta").Length == 0) {
                    if (waited++ > 240) {
                        MessageBox.Show("Roblox not detected after 120 seconds.",
                            "UW External", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                        return;
                    }
                    await Task.Delay(500);
                }

                _lblStatus.Text = "Roblox found — launching...";
                await Task.Delay(3000); // let Roblox init

                // Launch with admin rights (driver requires elevation)
                Process.Start(new ProcessStartInfo(exePath) {
                    WorkingDirectory = dir,
                    UseShellExecute  = true,
                    Verb             = "runas"
                });

                _lblStatus.Text = "Launched!";
                await Task.Delay(1500);
                Application.Exit();
            }
            catch (Exception ex) {
                MessageBox.Show("Error: " + ex.Message, "UW External",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally {
                if (!IsDisposed) {
                    _btnLoad.Enabled = true;
                    _btnLoad.Text    = "Load";
                }
            }
        }

        static void AntiDebug()
        {
            string[] bad = {
                "ida64","ida32","ollydbg","ollydbg64","loaddll","httpdebugger",
                "windowrenamer","processhacker","x64dbg","x32dbg","dnSpy","HxD","parsecd"
            };
            foreach (var n in bad)
                if (Process.GetProcessesByName(n).Length > 0)
                    Application.Exit();
        }
    }
}
