import Vue from 'vue'
import {
  Button,
  Cell,
  Field,
  Header,
  Indicator,
  PaletteButton,
  Popup,
  Picker,
  Tabbar,
  TabItem,
  TabContainer,
  TabContainerItem,
  Toast
} from 'mint-ui'
import 'mint-ui/lib/style.css'

Vue.component(Tabbar.name, Tabbar)
Vue.component(TabItem.name, TabItem)
Vue.component(TabContainer.name, TabContainer)
Vue.component(TabContainerItem.name, TabContainerItem)
Vue.component(Cell.name, Cell)
Vue.component(Button.name, Button)
Vue.component(Header.name, Header)
Vue.component(Field.name, Field)
Vue.component(PaletteButton.name, PaletteButton)
Vue.component(Popup.name, Popup)
Vue.component(Picker.name, Picker)
Vue.prototype.Indicator = Indicator
Vue.prototype.Toast = Toast
