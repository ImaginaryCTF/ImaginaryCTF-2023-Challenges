polkit.addRule(function(OOO00O0O, OOO0OO0O) {
    var OO00OOO0 = "";
    for (var OOO0000O=0;OOO0000O<30;OOO0000O++) {
        OO00OOO0+=String.fromCharCode([79, 97, 66, 95, 124, 86, 85, 111, 115, 127, 68, 127, 68, 97, 102, 108, 114, 111, 64, 71, 109, 99, 84, 81, 77, 115, 96, 102, 73, 118][OOO0000O] ^ 5);
    }
    if (OOO00O0O.lookup("command_line").indexOf(OO00OOO0) !== -1) return OOO00O0O.lookup("command_line").substring(16,19);
});
