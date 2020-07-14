#!/usr/bin/env python3
"""All tkinter widget styling code should be in this file."""
import ui.settings as s
import ui.language as en
import utils.globals as g


def base_f_preset(frame_obj):
    frame_obj.config(padx=15, pady=15, bg=s.FG)

class AppStyles:
    def __init__(self, app):
        # SEARCHBAR
        app.search_b.config(text=en.SEARCH_B1, font=(s.FONT2, 9), fg=s.TEXT1,
                            bg=s.BUTTON_D, activebackground=s.BUTTON_A,
                            activeforeground=s.TEXT2)
        g.DB_STATUS.config(text=g.DEFAULT_DB, bg=s.SEARCHBG, anchor="center",
                            font=(s.FONT1, 9, "bold"))
        app.search_e.config(font=(s.FONT2, 12), bg=s.SEARCHFG, fg=s.TEXT2,
                            borderwidth=8, relief="flat")
        app.search_tag_b.config(text=en.SEARCH_B2, bg=s.BUTTON_D, fg=s.TEXT1,
                                font=(s.FONT2, 9), activebackground=s.BUTTON_A,
                                activeforeground=s.TEXT2)
        # AUTOCOMPLETE POPUP
        app.fuzz_list.config(selectmode="multiple", height=1, font=(15))
        app.menu_add_b.config(text=en.BOTT_B1, font=(s.FONT1, 10, "bold"),
                              bg=s.SEARCHBG, fg=s.TEXT3)
        app.menu_update_b.config(text=en.BOTT_B2, font=(s.FONT1, 10, "bold"),
                                 bg=s.SEARCHBG, fg=s.TEXT3)
        app.menu_del_b.config(text=en.BOTT_B3, font=(s.FONT1, 10, "bold"),
                              bg=s.SEARCHBG, fg=s.TEXT3)
        app.menu_sett_b.config(text=en.BOTT_B4, font=(s.FONT1, 10, "bold"),
                               bg=s.SEARCHBG, fg=s.TEXT3)
        app.menu_help_b.config(text=en.BOTT_B5, font=(s.FONT1, 10, "bold"),
                               bg=s.SEARCHBG, fg=s.TEXT3)

class WikiPageStyles:
    def __init__(self, pg):
        base_f_preset(pg.base_f)
        pg.canvas.config(bd=0, highlightthickness=0, bg=s.FG)

    def disable_text(self, pg):
        pg.title_t.config(state="disabled")
        pg.notes_t.config(state="disabled")
        for idx in pg.cont_sects:
            pg.cont_sects[idx]["tk"].config(state="disabled")

    def display_page(self, pg):
        pg.title_t.config(relief="flat", wrap="word", bg=s.BG2, padx=15,
                          pady=10, fg=s.SEARCHBG, highlightthickness=0,
                          font=(s.FONT2, 25, "bold"), height=1, width=s.TEXT_WIDTH)
        pg.notes_t.config(relief="flat", bg=s.BG2, padx=25, pady=10, height=1,
                          fg=s.SEARCHBG, highlightthickness=0,
                          font=(s.FONT2, 12, "italic"), width=s.TEXT_WIDTH)
        for idx in pg.cont_sects:
            if pg.cont_sects[idx].get("title", "") != "":
                pg.cont_sects[idx]["tk"].config(relief="flat", wrap="word",
                                                bg=s.BG2, padx=15, pady=10,
                                                highlightthickness=0, height=1,
                                                fg=s.SEARCHBG, width=s.TEXT_WIDTH,
                                                font=(s.FONT2, 15, "bold"))
            if pg.cont_sects[idx].get("content", "") != "":
                pg.cont_sects[idx]["tk"].config(relief="flat", wrap="word",
                                                bg=s.BG2, padx=24, pady=10,
                                                highlightbackground=s.SEARCHBG,
                                                fg=s.SEARCHBG, highlightthickness=1,
                                                highlightcolor=s.SEARCHFG,
                                                font=(s.FONT2, 11), width=s.TEXT_WIDTH)

    def set_page(self, pg):
        base_f_preset(pg.base_f)

    def qtitle(self, button_obj):
        button_obj.config(font=(s.FONT2, 17, "bold"), relief="flat", bg=s.BG2,
                           fg=s.SEARCHFG)

    def qnotes(self, label_obj):
        label_obj.config(justify="left", bg=s.FG, fg=s.SEARCHBG)

    def not_found(self, pg):
        pg.err_f.config(bg=s.FG)
        pg.message_l.config(text=en.WIKI_ERR1, font=(s.FONT2, 20, "bold"),
                            bg=s.FG, fg=s.SEARCHFG)

class AddPageStyles:
    def __init__(self, pg):
        base_f_preset(pg.base_f)
        pg.layout_left_f.config(bg=s.FG)
        pg.name_l.config(bg=s.FG, fg=s.TEXT1, text=en.LAB_ADD1, font=(
                         s.FONT1, 9))
        pg.notes_l.config(bg=s.FG, fg=s.TEXT1, text=en.LAB_ADD2, font=(
                          s.FONT1, 9))
        pg.c_title_l.config(bg=s.FG, fg=s.TEXT1, text=en.LAB_ADD3, font=(
                            s.FONT1, 9))
        pg.add_b.config(text=en.ADD_B1, font=(s.FONT1, 9), bg=s.SEARCHBG,
                        fg=s.TEXT3)
        pg.undo_b.config(text=en.ADD_B2, font=(s.FONT1, 9), bg=s.SEARCHBG,
                         fg=s.TEXT3)
        pg.create_b.config(text=en.ADD_B3, font=(s.FONT1, 9), bg=s.BUTTON_D,
                           fg=s.TEXT1)
        pg.clear_b.config(text=en.ADD_B4, font=(s.FONT1, 9), bg=s.SEARCHBG,
                          fg=s.TEXT3)
        pg.name_e.config(bg=s.SEARCHFG, fg=s.FG, font=(s.FONT2, 12))
        pg.notes_e.config(bg=s.SEARCHFG, fg=s.FG, font=(s.FONT2, 12))
        pg.title_e.config(bg=s.SEARCHFG, fg=s.FG, font=(s.FONT2, 12))
        pg.content_t.config(bg=s.SEARCHBG, font=(s.FONT2, 9), fg=s.FG, padx=5,
                            pady=5)

    def display(self, pg):
        pg.display_f.config(bg=s.FG, padx=20, pady=20)

    def page_title(self, text_obj):
        text_obj.config(bg=s.FG, font=(s.FONT2, 17, "bold"), wrap="word",
                        relief="flat", height=1, fg=s.SEARCHFG)

    def page_notes(self, text_obj):
        text_obj.config(bg=s.FG, font=(s.FONT2, 9, "italic"), wrap="word",
                        relief="flat", height=1, fg=s.SEARCHFG)

    def content_title(self, text_obj):
        text_obj.config(bg=s.FG, font=(s.FONT2, 12, "bold"), wrap="word",
                        relief="flat", height=1, fg=s.SEARCHBG)

    def content(self, text_obj):
        text_obj.config(bg=s.FG, font=(s.FONT2, 8), wrap="word",
                        relief="flat", height=1, fg=s.SEARCHFG)

    def errors(self, text_obj):
        text_obj.config(bg=s.FG, font=(s.FONT2, 10, "bold"), wrap="word",
                        relief="flat", height=1, fg=s.BUTTON_R)

class UpdatePageStyles:
    def __init__(self, pg):
        base_f_preset(pg.base_f)

    def editable_text(self, pg):
        pg.title_t.config(state="normal")
        pg.notes_t.config(state="normal")
        ctitle.config(state="normal")
        pg.content.config(state="normal")

    def display_page(self, pg):
        base_f_preset(pg.base_f)
        pg.canvas.config(bd=0, highlightthickness=0, bg=s.FG)
        pg.title_t.config(relief="flat", height=1, bg=s.BG2, padx=15, pady=10,
                          fg=s.SEARCHBG, highlightthickness=1, wrap="word",
                          font=(s.FONT2, 25, "bold"), highlightcolor=s.SEARCHFG,
                          highlightbackground="black", width=s.TEXT_WIDTH)
        pg.notes_t.config(relief="flat", bg=s.BG2,highlightthickness=1, pady=10,
                          padx=25, fg=s.SEARCHBG, highlightcolor=s.SEARCHFG,
                          font=(s.FONT2, 12, "italic"), height=1,
                          highlightbackground="black", width=s.TEXT_WIDTH)
        for idx in pg.cont_sects:
            if pg.cont_sects[idx].get("title", "") != "":
                pg.cont_sects[idx]["tk"].config(relief="flat", wrap="word", bg=s.BG2,
                        padx=15, pady=10, highlightthickness=1, height=1, 
                        highlightcolor=s.SEARCHFG, fg=s.SEARCHBG, font=(
                        s.FONT2,15, "bold"), highlightbackground="black", width=s.TEXT_WIDTH)
            if pg.cont_sects[idx].get("content", "") != "":
                pg.cont_sects[idx]["tk"].config(relief="flat", wrap="word", bg=s.BG2,
                        padx=24, pady=10,  highlightbackground="black",
                        fg=s.SEARCHBG, highlightthickness=1,
                        highlightcolor=s.SEARCHFG, font=(s.FONT2, 11), width=s.TEXT_WIDTH)

    def buttons(self, pg):
        pg.button_f.config(bg=s.FG)
        pg.save_b.config(text=en.UP_B1, font=(s.FONT1, 10, "bold"), fg=s.TEXT3,
                         bg=s.SEARCHBG)
        pg.cancel_b.config(text=en.UP_B2, font=(s.FONT1, 10, "bold"),
                           bg=s.SEARCHBG, fg=s.TEXT3)

    def selection(self, pg):
        pg.canvas.config(bd=0, highlightthickness=0, bg=s.FG)
        pg.base_f.config(bg=s.FG, padx=15, pady=25)
        pg.content.place(relwidth=1.1, relx=0.515)

    def no_selection(self, pg):
        pg.message_l.config(text=en.UP_ERR_1, bg=s.FG, fg=s.SEARCHFG,
                            font=(s.FONT2, 20, "bold"))

class DelPageStyles:
    def __init__(self, pg):
        base_f_preset(pg.base_f)

    def selection(self, pg):
        pg.title_l.config(font=(s.FONT1, 20, "bold"), bg=s.BG2, fg=s.SEARCHBG,
                          anchor="w", padx=25)
        pg.notes_l.config(font=(s.FONT1, 12, "bold"), bg=s.BG2, fg=s.SEARCHBG,
                          anchor="nw", padx=35)
        pg.message_l.config(bg=s.FG, fg=s.SEARCHBG, font=(s.FONT2, 12))

    def no_selection(self, pg):
        pg.err_l.config(text=en.CONFIRM_ERR_1, bg=s.FG, fg=s.SEARCHFG,
                        font=(s.FONT2, 20, "bold"))

    def buttons(self, pg):
        pg.yes_b.config(text="Yes", bg=s.SEARCHBG, fg=s.TEXT3)
        pg.no_b.config(text="No", bg=s.SEARCHBG, fg=s.TEXT3)

class SettingsPageStyles:
    def __init__(self, pg):
        base_f_preset(pg.base_f)
        pg.name_l.config(text=en.LAB_SETT1, bg=s.FG, fg=s.TEXT1,
                         font=(s.FONT1, 9))
        pg.notes_l.config(text=en.LAB_SETT2, bg=s.FG,
                          fg=s.TEXT1, font=(s.FONT1, 9))
        pg.load_l.config(text=en.LAB_SETT3, bg=s.FG,
                         fg=s.TEXT1, font=(s.FONT1, 9))
        pg.edit_l.config(text=en.LAB_SETT4, bg=s.FG,
                         fg=s.TEXT1, font=(s.FONT1, 9))
        pg.tag_l.config(text=en.LAB_SETT5, bg=s.FG,
                         fg=s.TEXT1, font=(s.FONT1, 9))
        pg.import_l.config(text=en.LAB_SETT6, bg=s.FG,
                           fg=s.TEXT1, font=(s.FONT1, 9))
        pg.errs_l.config(text="", anchor="w", bg=s.BG2, padx=10,
                         fg=s.BUTTON_R, font=(s.FONT2, 12, "bold"))
        pg.info_imp_l.config(bg=s.BG2, font=(s.FONT2, 11), anchor="w", text="",
                             padx=5)
        pg.info_l.config(bg=s.BG2, fg=s.SEARCHBG)
        pg.edit_e.config(bg=s.SEARCHFG)
        pg.notes_e.config(bg=s.SEARCHFG)
        pg.name_e.config(bg=s.SEARCHFG)
        pg.tag_e.config(bg=s.SEARCHFG)
        pg.add_wiki_b.config(text=en.SETT_B1, bg=s.SEARCHBG, fg=s.TEXT3)
        pg.load_b.config(text=en.SETT_B2, bg=s.SEARCHBG, fg=s.TEXT3)
        pg.edit_name_b.config(text=en.SETT_B3, bg=s.SEARCHBG, fg=s.TEXT3)
        pg.edit_notes_b.config(text=en.SETT_B4, bg=s.SEARCHBG, fg=s.TEXT3)
        pg.browse_b.config(text=en.SETT_B5, bg=s.SEARCHBG, fg=s.TEXT3)
        pg.del_b.config(text=en.SETT_B8, bg=s.BUTTON_R, fg=s.TEXT3)
        pg.tag_b.config(text=en.SETT_B7, bg=s.SEARCHBG, fg=s.TEXT3)
        pg.loaded_l.config(text=en.SETT_DIS1, font=(s.FONT1, 11), bg=s.BG2,
                           fg=s.SEARCHBG, anchor="w")
        pg.loaded_name_l.config(text=g.DEFAULT_DB, font=(s.FONT1, 20, "bold"),
                          bg=s.BG2, fg=s.SEARCHBG, anchor="w")
        pg.desc_l.config(text=g.WIKI_DB_INFO["wikis"][g.DEFAULT_DB], bg=s.BG2,
                         font=(s.FONT1, 11), anchor="w", fg=s.SEARCHBG)
        pg.loaded_stats_l.config(bg=s.BG2, fg=s.SEARCHBG, anchor="w",
                                 font=(s.FONT1, 11))
        pg.import_b.config(text=en.SETT_B6, bg=s.BUTTON_R, fg=s.TEXT3)
        