var SideBar = (() => {
    function SideBar() {
        var self = this;
        var sideBar = $('#products-filter');
        var backDrop = $('#backdrop');

        backDrop.click(function() {
            self.hideMobile();
        });

        this.toggle = function() {
            sideBar.toggleClass('open-mobile');
            backDrop.toggleClass('open');
        }
        
        this.hideMobile = function() {
            sideBar.removeClass('open-mobile');
            backDrop.removeClass('open');
        }

        this.show = function() {
            sideBar.addClass('open');
        }

        this.hide = function() {
            sideBar.removeClass('open');
            sideBar.removeClass('open-mobile');
            backDrop.removeClass('open');
        }
    }
    return new SideBar()
})();

var MobileMenuBar = (() => {
    function MobileMenuBar() {
        var self = this;
        var menuBar = $('#mobile-menu-sidebar');
        var backDrop = $('#backdrop');

        backDrop.click(function() {
            self.hide();
        });

        this.toggle = function() {
            menuBar.toggleClass('open');
            backDrop.toggleClass('open');
        }

        this.hide = function() {
            menuBar.removeClass('open');
            backDrop.removeClass('open');
        }

        this.show = function() {
            menuBar.addClass('open');
            backDrop.addClass('open');
        }
    }
    return new MobileMenuBar()
})();