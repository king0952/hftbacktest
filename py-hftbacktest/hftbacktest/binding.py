from ctypes import (
    c_void_p,
    c_bool,
    c_float,
    c_double,
    c_uint8,
    c_uint64,
    c_int32,
    c_int64,
    POINTER,
    CDLL
)
from typing import Tuple, Any

import numba
import numpy as np
from numba import (
    carray,
    uint64,
    int64,
    float64,
    int32,
    float32,
    uint8,
)
from numba.core.types import voidptr
from numba.experimental import jitclass

from . import _hftbacktest
from .intrinsic import ptr_from_val, address_as_void_pointer, val_from_ptr, is_null_ptr
from .order import order_dtype, Order, Order_


state_values_dtype = np.dtype([
    ('position', 'f8'),
    ('balance', 'f8'),
    ('fee', 'f8'),
    ('trading_volume', 'f8'),
    ('trading_value', 'f8'),
    ('num_trades', 'i4'),
])

event_dtype = np.dtype([
    ('ev', 'i8'),
    ('exch_ts', 'i8'),
    ('local_ts', 'i8'),
    ('px', 'f4'),
    ('qty', 'f4')
])

EVENT_ARRAY = np.ndarray[Any, event_dtype]

lib = CDLL(_hftbacktest.__file__)

hashmapdepth_best_bid_tick = lib.hashmapdepth_best_bid_tick
hashmapdepth_best_bid_tick.restype = c_int32
hashmapdepth_best_bid_tick.argtypes = [c_void_p]

hashmapdepth_best_ask_tick = lib.hashmapdepth_best_ask_tick
hashmapdepth_best_ask_tick.restype = c_int32
hashmapdepth_best_ask_tick.argtypes = [c_void_p]

hashmapdepth_best_bid = lib.hashmapdepth_best_bid
hashmapdepth_best_bid.restype = c_float
hashmapdepth_best_bid.argtypes = [c_void_p]

hashmapdepth_best_ask = lib.hashmapdepth_best_ask
hashmapdepth_best_ask.restype = c_float
hashmapdepth_best_ask.argtypes = [c_void_p]

hashmapdepth_tick_size = lib.hashmapdepth_tick_size
hashmapdepth_tick_size.restype = c_float
hashmapdepth_tick_size.argtypes = [c_void_p]

hashmapdepth_lot_size = lib.hashmapdepth_lot_size
hashmapdepth_lot_size.restype = c_float
hashmapdepth_lot_size.argtypes = [c_void_p]

hashmapdepth_bid_qty_at_tick = lib.hashmapdepth_bid_qty_at_tick
hashmapdepth_bid_qty_at_tick.restype = c_float
hashmapdepth_bid_qty_at_tick.argtypes = [c_void_p, c_int32]

hashmapdepth_ask_qty_at_tick = lib.hashmapdepth_ask_qty_at_tick
hashmapdepth_ask_qty_at_tick.restype = c_float
hashmapdepth_ask_qty_at_tick.argtypes = [c_void_p, c_int32]

hashmapdepth_snapshot = lib.hashmapdepth_snapshot
hashmapdepth_snapshot.restype = c_void_p
hashmapdepth_snapshot.argtypes = [c_void_p, POINTER(c_uint64)]

hashmapdepth_snapshot_free = lib.hashmapdepth_snapshot_free
hashmapdepth_snapshot_free.restype = c_void_p
hashmapdepth_snapshot_free.argtypes = [c_void_p, c_uint64]


class HashMapMarketDepth:
    ptr: voidptr

    def __init__(self, ptr: voidptr):
        self.ptr = ptr

    @property
    def best_bid_tick(self) -> int32:
        """
        Returns the best bid price in ticks.
        """
        return hashmapdepth_best_bid_tick(self.ptr)

    @property
    def best_ask_tick(self) -> int32:
        """
        Returns the best ask price in ticks.
        """
        return hashmapdepth_best_ask_tick(self.ptr)

    @property
    def best_bid(self) -> float32:
        """
        Returns the best bid price.
        """
        return hashmapdepth_best_bid(self.ptr)

    @property
    def best_ask(self) -> float32:
        """
        Returns the best ask price.
        """
        return hashmapdepth_best_ask(self.ptr)

    @property
    def tick_size(self) -> float32:
        """
        Returns the tick size.
        """
        return hashmapdepth_tick_size(self.ptr)

    @property
    def lot_size(self) -> float32:
        """
        Returns the lot size.
        """
        return hashmapdepth_lot_size(self.ptr)

    def bid_qty_at_tick(self, price_tick: int32) -> float32:
        """
        Returns the quantity at the bid market depth for a given price in ticks.

        Args:
            price_tick: Price in ticks.

        Returns:
            The quantity at the specified price.
        """
        return hashmapdepth_bid_qty_at_tick(self.ptr, price_tick)

    def ask_qty_at_tick(self, price_tick: int32) -> float32:
        """
        Returns the quantity at the ask market depth for a given price in ticks.

        Args:
            price_tick: Price in ticks.

        Returns:
            The quantity at the specified price.
        """
        return hashmapdepth_ask_qty_at_tick(self.ptr, price_tick)

    def snapshot(self) -> EVENT_ARRAY:
        length = uint64(0)
        len_ptr = ptr_from_val(length)
        ptr = hashmapdepth_snapshot(self.ptr, len_ptr)
        return numba.carray(
            address_as_void_pointer(ptr),
            val_from_ptr(len_ptr),
            event_dtype
        )

    def snapshot_free(self, arr: EVENT_ARRAY):
        hashmapdepth_snapshot_free(arr.ctypes.data, len(arr))


HashMapMarketDepth_ = jitclass(HashMapMarketDepth)


roivecdepth_best_bid_tick = lib.roivecdepth_best_bid_tick
roivecdepth_best_bid_tick.restype = c_int32
roivecdepth_best_bid_tick.argtypes = [c_void_p]

roivecdepth_best_ask_tick = lib.roivecdepth_best_ask_tick
roivecdepth_best_ask_tick.restype = c_int32
roivecdepth_best_ask_tick.argtypes = [c_void_p]

roivecdepth_best_bid = lib.roivecdepth_best_bid
roivecdepth_best_bid.restype = c_float
roivecdepth_best_bid.argtypes = [c_void_p]

roivecdepth_best_ask = lib.roivecdepth_best_ask
roivecdepth_best_ask.restype = c_float
roivecdepth_best_ask.argtypes = [c_void_p]

roivecdepth_tick_size = lib.roivecdepth_tick_size
roivecdepth_tick_size.restype = c_float
roivecdepth_tick_size.argtypes = [c_void_p]

roivecdepth_lot_size = lib.roivecdepth_lot_size
roivecdepth_lot_size.restype = c_float
roivecdepth_lot_size.argtypes = [c_void_p]

roivecdepth_bid_qty_at_tick = lib.roivecdepth_bid_qty_at_tick
roivecdepth_bid_qty_at_tick.restype = c_float
roivecdepth_bid_qty_at_tick.argtypes = [c_void_p, c_int32]

roivecdepth_ask_qty_at_tick = lib.roivecdepth_ask_qty_at_tick
roivecdepth_ask_qty_at_tick.restype = c_float
roivecdepth_ask_qty_at_tick.argtypes = [c_void_p, c_int32]

roivecdepth_bid_depth = lib.roivecdepth_bid_depth
roivecdepth_bid_depth.restype = c_void_p
roivecdepth_bid_depth.argtypes = [c_void_p, POINTER(c_uint64)]

roivecdepth_ask_depth = lib.roivecdepth_ask_depth
roivecdepth_ask_depth.restype = c_void_p
roivecdepth_ask_depth.argtypes = [c_void_p, POINTER(c_uint64)]


class ROIVectorMarketDepth:
    ptr: voidptr

    def __init__(self, ptr: voidptr):
        self.ptr = ptr

    @property
    def best_bid_tick(self) -> int32:
        """
        Returns the best bid price in ticks.
        """
        return roivecdepth_best_bid_tick(self.ptr)

    @property
    def best_ask_tick(self) -> int32:
        """
        Returns the best ask price in ticks.
        """
        return roivecdepth_best_ask_tick(self.ptr)

    @property
    def best_bid(self) -> float32:
        """
        Returns the best bid price.
        """
        return roivecdepth_best_bid(self.ptr)

    @property
    def best_ask(self) -> float32:
        """
        Returns the best ask price.
        """
        return roivecdepth_best_ask(self.ptr)

    @property
    def tick_size(self) -> float32:
        """
        Returns the tick size.
        """
        return roivecdepth_tick_size(self.ptr)

    @property
    def lot_size(self) -> float32:
        """
        Returns the lot size.
        """
        return roivecdepth_lot_size(self.ptr)

    def bid_qty_at_tick(self, price_tick: int32) -> float32:
        """
        Returns the quantity at the bid market depth for a given price in ticks.

        Args:
            price_tick: Price in ticks.

        Returns:
            The quantity at the specified price.
        """
        return roivecdepth_bid_qty_at_tick(self.ptr, price_tick)

    def ask_qty_at_tick(self, price_tick: int32) -> float32:
        """
        Returns the quantity at the ask market depth for a given price in ticks.

        Args:
            price_tick: Price in ticks.

        Returns:
            The quantity at the specified price.
        """
        return roivecdepth_ask_qty_at_tick(self.ptr, price_tick)

    def bid_depth(self) -> np.ndarray[Any, float32]:
        length = uint64(0)
        len_ptr = ptr_from_val(length)
        ptr = roivecdepth_bid_depth(self.ptr, len_ptr)
        return numba.carray(
            address_as_void_pointer(ptr),
            val_from_ptr(len_ptr),
            float32
        )

    def ask_depth(self) -> np.ndarray[Any, float32]:
        length = uint64(0)
        len_ptr = ptr_from_val(length)
        ptr = roivecdepth_ask_depth(self.ptr, len_ptr)
        return numba.carray(
            address_as_void_pointer(ptr),
            val_from_ptr(len_ptr),
            float32
        )


ROIVectorMarketDepth_ = jitclass(ROIVectorMarketDepth)

orders_get = lib.orders_get
orders_get.restype = c_void_p
orders_get.argtypes = [c_void_p, c_int64]

orders_contains = lib.orders_contains
orders_contains.restype = c_bool
orders_contains.argtypes = [c_void_p, c_int64]

orders_len = lib.orders_len
orders_len.restype = c_uint64
orders_len.argtypes = [c_void_p]

orders_values = lib.orders_values
orders_values.restype = c_void_p
orders_values.argtypes = [c_void_p]

orders_values_next = lib.orders_values_next
orders_values_next.restype = c_void_p
orders_values_next.argtypes = [c_void_p]


class Values:
    ptr: voidptr

    def __init__(self, ptr: voidptr):
        self.ptr = ptr

    # def __next__(self) -> Order:
    #     if is_null_ptr(self.ptr):
    #         return None
    #     order_ptr = orders_values_next(self.ptr)
    #     if is_null_ptr(order_ptr):
    #         self.ptr = 0
    #         raise StopIteration
    #     else:
    #         arr = carray(
    #             address_as_void_pointer(order_ptr),
    #             1,
    #             dtype=order_dtype
    #         )
    #         return Order_(arr)

    def next(self) -> Order | None:
        if is_null_ptr(self.ptr):
            return None
        order_ptr = orders_values_next(self.ptr)
        if is_null_ptr(order_ptr):
            self.ptr = 0
            return None
        else:
            arr = carray(
                address_as_void_pointer(order_ptr),
                1,
                dtype=order_dtype
            )
            return Order_(arr)


Values_ = jitclass(Values)


class OrderDict:
    """
    This is a wrapper for the order dictionary. It only supports :func:`get` method, ``in`` operator through
    :func:`__contains__`, and :func:`values` method for iterating over values. Please note the limitations of the values
    iterator.
    """
    ptr: voidptr

    def __init__(self, ptr: voidptr):
        self.ptr = ptr

    def values(self) -> Values:
        """
        Since `numba` does not support ``__next__`` method in `njit`, you need to manually iterate using the
        ``next``, which returns the next order value if it exists; otherwise, it returns `None`.

        **Example**

        .. code-block:: python

            values = order_dict.values()
            while True:
                order = values.next()
                if order is None:
                    break
                # Do what you need with the order.

        """
        return Values_(orders_values(self.ptr))

    def get(self, order_id: int64) -> Order | None:
        """
        Args:
            order_id: Order ID

        Returns:
            Order with the specified order ID; `None` if it does not exist.
        """
        order_ptr = orders_get(self.ptr, order_id)
        if is_null_ptr(order_ptr):
            return None
        else:
            arr = carray(
                address_as_void_pointer(order_ptr),
                1,
                dtype=order_dtype
            )
            return Order_(arr)

    def __len__(self) -> uint64:
        return orders_len(self.ptr)

    def __contains__(self, order_id: int64) -> bool:
        """
        Args:
            order_id: Order ID
        Returns:
            `True` if the order with the specified order ID exists; otherwise, `False`.
        """
        return orders_contains(self.ptr, order_id)


OrderDict_ = jitclass(OrderDict)

hashmapbt_elapse = lib.hashmapbt_elapse
hashmapbt_elapse.restype = c_int64
hashmapbt_elapse.argtypes = [c_void_p, c_uint64]

hashmapbt_elapse_bt = lib.hashmapbt_elapse_bt
hashmapbt_elapse_bt.restype = c_int64
hashmapbt_elapse_bt.argtypes = [c_void_p, c_uint64]

hashmapbt_hashmapbt_wait_order_response = lib.hashmapbt_wait_order_response
hashmapbt_hashmapbt_wait_order_response.restype = c_int64
hashmapbt_hashmapbt_wait_order_response.argtypes = [c_void_p, c_uint64, c_int64, c_int64]

hashmapbt_wait_next_feed = lib.hashmapbt_wait_next_feed
hashmapbt_wait_next_feed.restype = c_int64
hashmapbt_wait_next_feed.argtypes = [c_void_p, c_bool, c_int64]

hashmapbt_close = lib.hashmapbt_close
hashmapbt_close.restype = c_int64
hashmapbt_close.argtypes = [c_void_p]

hashmapbt_position = lib.hashmapbt_position
hashmapbt_position.restype = c_double
hashmapbt_position.argtypes = [c_void_p, c_uint64]

hashmapbt_current_timestamp = lib.hashmapbt_current_timestamp
hashmapbt_current_timestamp.restype = c_int64
hashmapbt_current_timestamp.argtypes = [c_void_p]

hashmapbt_depth_typed = lib.hashmapbt_depth_typed
hashmapbt_depth_typed.restype = c_void_p
hashmapbt_depth_typed.argtypes = [c_void_p, c_uint64]

hashmapbt_trade_typed = lib.hashmapbt_trade_typed
hashmapbt_trade_typed.restype = c_void_p
hashmapbt_trade_typed.argtypes = [c_void_p, c_uint64, POINTER(c_uint64)]

hashmapbt_num_assets = lib.hashmapbt_num_assets
hashmapbt_num_assets.restype = c_uint64
hashmapbt_num_assets.argtypes = [c_void_p]

hashmapbt_submit_buy_order = lib.hashmapbt_submit_buy_order
hashmapbt_submit_buy_order.restype = c_int64
hashmapbt_submit_buy_order.argtypes = [
    c_void_p,
    c_uint64,
    c_int64,
    c_float,
    c_float,
    c_uint8,
    c_uint8,
    c_bool
]

hashmapbt_submit_sell_order = lib.hashmapbt_submit_sell_order
hashmapbt_submit_sell_order.restype = c_int64
hashmapbt_submit_sell_order.argtypes = [
    c_void_p,
    c_uint64,
    c_int64,
    c_float,
    c_float,
    c_uint8,
    c_uint8,
    c_bool
]

hashmapbt_cancel = lib.hashmapbt_cancel
hashmapbt_cancel.restype = c_int64
hashmapbt_cancel.argtypes = [c_void_p, c_uint64, c_int64, c_bool]

hashmapbt_clear_last_trades = lib.hashmapbt_clear_last_trades
hashmapbt_clear_last_trades.restype = c_void_p
hashmapbt_clear_last_trades.argtypes = [c_void_p, c_uint64]

hashmapbt_clear_inactive_orders = lib.hashmapbt_clear_inactive_orders
hashmapbt_clear_inactive_orders.restype = c_void_p
hashmapbt_clear_inactive_orders.argtypes = [c_void_p, c_uint64]

hashmapbt_orders = lib.hashmapbt_orders
hashmapbt_orders.restype = c_void_p
hashmapbt_orders.argtypes = [c_void_p, c_uint64]

hashmapbt_state_values = lib.hashmapbt_state_values
hashmapbt_state_values.restype = c_void_p
hashmapbt_state_values.argtypes = [c_void_p, c_uint64]

hashmapbt_feed_latency = lib.hashmapbt_feed_latency
hashmapbt_feed_latency.restype = c_bool
hashmapbt_feed_latency.argtypes = [c_void_p, c_uint64, POINTER(c_int64), POINTER(c_int64)]

hashmapbt_order_latency = lib.hashmapbt_order_latency
hashmapbt_order_latency.restype = c_bool
hashmapbt_order_latency.argtypes = [c_void_p, c_uint64, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)]

hashmapbt_goto_end = lib.hashmapbt_goto_end
hashmapbt_goto_end.restype = c_int64
hashmapbt_goto_end.argtypes = [c_void_p]


class HashMapMarketDepthMultiAssetMultiExchangeBacktest:
    ptr: voidptr

    def __init__(self, ptr: voidptr):
        self.ptr = ptr

    @property
    def current_timestamp(self) -> int64:
        """
        In backtesting, this timestamp reflects the time at which the backtesting is conducted within the provided data.
        """
        return hashmapbt_current_timestamp(self.ptr)

    def depth_typed(self, asset_no: uint64) -> HashMapMarketDepth:
        """
        Args:
            asset_no: Asset number from which the market depth will be retrieved.

        Returns:
            The depth of market of the specific asset.
        """
        return HashMapMarketDepth_(hashmapbt_depth_typed(self.ptr, asset_no))

    @property
    def num_assets(self) -> uint64:
        """
        Returns the number of assets.
        """
        return hashmapbt_num_assets(self.ptr)

    def position(self, asset_no: uint64) -> float64:
        """
        Args:
            asset_no: Asset number from which the position will be retrieved.

        Returns:
            The quantity of the held position.
        """
        return hashmapbt_position(self.ptr, asset_no)

    def state_values(self, asset_no: uint64) -> state_values_dtype:
        """
        Args:
            asset_no: Asset number from which the state values will be retrieved.

        Returns:
            The state’s values.
        """
        ptr = hashmapbt_state_values(self.ptr, asset_no)
        return numba.carray(
            address_as_void_pointer(ptr),
            1,
            state_values_dtype
        )

    def trade_typed(self, asset_no: uint64) -> EVENT_ARRAY:
        """
        Args:
            asset_no: Asset number from which the trades will be retrieved.

        Returns:
            An array of `Event` representing trades occurring in the market for the specific asset.
        """
        length = uint64(0)
        len_ptr = ptr_from_val(length)
        ptr = hashmapbt_trade_typed(self.ptr, asset_no, len_ptr)
        return numba.carray(
            address_as_void_pointer(ptr),
            val_from_ptr(len_ptr),
            event_dtype
        )

    def clear_last_trades(self, asset_no: uint64) -> None:
        """
        Clears the last trades occurring in the market from the buffer for :func:`trade_typed`.

        Args:
            asset_no: Asset number at which this command will be executed. If :const:`ALL_ASSETS`, all last trades in
                      any assets will be cleared.
        """
        hashmapbt_clear_last_trades(self.ptr, asset_no)

    def orders(self, asset_no: uint64) -> OrderDict:
        """
        Args:
            asset_no: Asset number from which orders will be retrieved.

        Returns:
            An order dictionary where the keys are order IDs and the corresponding values are :class:`Order`s.
        """
        return OrderDict_(hashmapbt_orders(self.ptr, asset_no))

    def submit_buy_order(
            self,
            asset_no: uint64,
            order_id: int64,
            price: float32,
            qty: float32,
            time_in_force: uint8,
            order_type: uint8,
            wait: bool
    ) -> int64:
        """
        Submits a buy order.

        Args:
            asset_no: Asset number at which this command will be executed.
            order_id: The unique order ID; there should not be any existing order with the same ID on both local and
                      exchange sides.
            price: Order price.
            qty: Quantity to buy.
            time_in_force: Available options vary depending on the exchange model. See to the exchange model for
                           details.

                * :const:`GTC`
                * :const:`GTX`
                * :const:`FOK`
                * :const:`IOC`
            order_type: Available options vary depending on the exchange model. See to the exchange model for details.

                * :const:`LIMIT`
                * :const:`MARKET`
            wait: If `True`, wait until the order placement response is received.

        Returns:
            -1 when an error occurs; otherwise, it succeeds in submitting a buy order.
        """
        return hashmapbt_submit_buy_order(self.ptr, asset_no, order_id, price, qty, time_in_force, order_type, wait)

    def submit_sell_order(
            self,
            asset_no: uint64,
            order_id: int64,
            price: float32,
            qty: float32,
            time_in_force: uint8,
            order_type: uint8,
            wait: bool
    ) -> int64:
        """
        Submits a sell order.

        Args:
            asset_no: Asset number at which this command will be executed.
            order_id: The unique order ID; there should not be any existing order with the same ID on both local and
                      exchange sides.
            price: Order price.
            qty: Quantity to buy.
            time_in_force: Available options vary depending on the exchange model. See to the exchange model for
                           details.

                * :const:`GTC`
                * :const:`GTX`
                * :const:`FOK`
                * :const:`IOC`
            order_type: Available options vary depending on the exchange model. See to the exchange model for details.

                * :const:`LIMIT`
                * :const:`MARKET`
            wait: If `True`, wait until the order placement response is received.

        Returns:
            `-1` when an error occurs; otherwise, it succeeds in submitting a sell order.
        """
        return hashmapbt_submit_sell_order(self.ptr, asset_no, order_id, price, qty, time_in_force, order_type, wait)

    def cancel(self, asset_no: uint64, order_id: int64, wait: bool) -> int64:
        """
        Cancels the specified order.

        Args:
            asset_no: Asset number at which this command will be executed.
            order_id: Order ID to cancel.
            wait: If `True`, wait until the order cancel response is received.

        Returns:
            `-1` when an error occurs; otherwise, it successfully submits a cancel order.
        """
        return hashmapbt_cancel(self.ptr, asset_no, order_id, wait)

    def clear_inactive_orders(self, asset_no: uint64) -> None:
        """
        Clears inactive orders from the local order dictionary whose status is neither :const:`NEW` nor
        :const:`PARTIALLY_FILLED`.

        Args:
            asset_no: Asset number at which this command will be executed. If :const:`ALL_ASSETS`, all inactive orders
                      in any assets will be cleared.
        """
        hashmapbt_clear_inactive_orders(self.ptr, asset_no)

    def wait_order_response(self, asset_no: uint64, order_id: int64, timeout: int64) -> int64:
        """
        Waits for the response of the order with the given order ID until timeout.

        Args:
            asset_no: Asset number where an order with `order_id` exists.
            order_id: Order ID to wait for the response.
            timeout: Timeout for waiting for the order response. Nanoseconds is the default unit. However, unit should
                     be the same as the data’s timestamp unit.

        Returns:
            * `1` when it receives an order response for the specified order ID of the specified asset number.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return hashmapbt_hashmapbt_wait_order_response(self.ptr, asset_no, order_id, timeout)

    def wait_next_feed(self, include_order_resp: bool, timeout: int64) -> int64:
        """
        Waits until the next feed is received, or until timeout.

        Args:
            include_order_resp: If set to `True`, it will return when any order response is received, in addition to the
                                next feed.
            timeout: Timeout for waiting for the next feed or an order response. Nanoseconds is the default unit.
                     However, unit should be the same as the data’s timestamp unit.

        Returns:
            * `1` when it receives a feed or an order response.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return hashmapbt_wait_next_feed(self.ptr, include_order_resp, timeout)

    def elapse(self, duration: uint64) -> int64:
        """
        Elapses the specified duration.

        Args:
            duration: Duration to elapse. Nanoseconds is the default unit. However, unit should be the same as the
                      data’s timestamp unit.

        Returns:
            * `1` when it reaches the specified timestamp within the data.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return hashmapbt_elapse(self.ptr, duration)

    def elapse_bt(self, duration: int64) -> int64:
        """
        Elapses time only in backtesting. In live mode, it is ignored. (Supported only in the Rust implementation)

        The `elapse` method exclusively manages time during backtesting, meaning that factors such as computing time are
        not properly accounted for. So, this method can be utilized to simulate such processing times.

        Args:
            duration: Duration to elapse. Nanoseconds is the default unit. However, unit should be the same as the
                      data’s timestamp unit.

        Returns:
            * `1` when it reaches the specified timestamp within the data.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return hashmapbt_elapse_bt(self.ptr, duration)

    def close(self) -> int64:
        """
        Closes this backtester or bot.

        Returns:
            `-1` when an error occurs; otherwise, it successfully closes the bot.
        """
        return hashmapbt_close(self.ptr)

    def feed_latency(self, asset_no: uint64) -> Tuple[int64, int64] | None:
        """
        Args:
            asset_no: Asset number from which the last feed latency will be retrieved.

        Returns:
            The last feed’s exchange timestamp and local receipt timestamp if a feed has been received; otherwise,
            returns `None`.
        """
        exch_ts = int64(0)
        local_ts = int64(0)
        exch_ts_ptr = ptr_from_val(exch_ts)
        local_ts_ptr = ptr_from_val(local_ts)
        if hashmapbt_feed_latency(self.ptr, asset_no, exch_ts_ptr, local_ts_ptr):
            return val_from_ptr(exch_ts_ptr), val_from_ptr(local_ts_ptr)
        return None

    def order_latency(self, asset_no: uint64) -> Tuple[int64, int64, int64] | None:
        """
        Args:
            asset_no: Asset number from which the last order latency will be retrieved.

        Returns:
            The last order’s request timestamp, exchange timestamp, and response receipt timestamp if there has been an
            order submission; otherwise, returns `None`.
        """
        req_ts = int64(0)
        exch_ts = int64(0)
        resp_ts = int64(0)
        req_ts_ptr = ptr_from_val(req_ts)
        exch_ts_ptr = ptr_from_val(exch_ts)
        resp_ts_ptr = ptr_from_val(resp_ts)
        if hashmapbt_order_latency(self.ptr, asset_no, req_ts_ptr, exch_ts_ptr, resp_ts_ptr):
            return val_from_ptr(req_ts_ptr), val_from_ptr(exch_ts_ptr), val_from_ptr(resp_ts_ptr)
        return None

    def _goto_end(self) -> int64:
        return hashmapbt_goto_end(self.ptr)


HashMapMarketDepthMultiAssetMultiExchangeBacktest_ = jitclass(HashMapMarketDepthMultiAssetMultiExchangeBacktest)


roivecbt_elapse = lib.roivecbt_elapse
roivecbt_elapse.restype = c_int64
roivecbt_elapse.argtypes = [c_void_p, c_uint64]

roivecbt_elapse_bt = lib.roivecbt_elapse_bt
roivecbt_elapse_bt.restype = c_int64
roivecbt_elapse_bt.argtypes = [c_void_p, c_uint64]

roivecbt_roivecbt_wait_order_response = lib.roivecbt_wait_order_response
roivecbt_roivecbt_wait_order_response.restype = c_int64
roivecbt_roivecbt_wait_order_response.argtypes = [c_void_p, c_uint64, c_int64, c_int64]

roivecbt_wait_next_feed = lib.roivecbt_wait_next_feed
roivecbt_wait_next_feed.restype = c_int64
roivecbt_wait_next_feed.argtypes = [c_void_p, c_bool, c_int64]

roivecbt_close = lib.roivecbt_close
roivecbt_close.restype = c_int64
roivecbt_close.argtypes = [c_void_p]

roivecbt_position = lib.roivecbt_position
roivecbt_position.restype = c_double
roivecbt_position.argtypes = [c_void_p, c_uint64]

roivecbt_current_timestamp = lib.roivecbt_current_timestamp
roivecbt_current_timestamp.restype = c_int64
roivecbt_current_timestamp.argtypes = [c_void_p]

roivecbt_depth_typed = lib.roivecbt_depth_typed
roivecbt_depth_typed.restype = c_void_p
roivecbt_depth_typed.argtypes = [c_void_p, c_uint64]

roivecbt_trade_typed = lib.roivecbt_trade_typed
roivecbt_trade_typed.restype = c_void_p
roivecbt_trade_typed.argtypes = [c_void_p, c_uint64, POINTER(c_uint64)]

roivecbt_num_assets = lib.roivecbt_num_assets
roivecbt_num_assets.restype = c_uint64
roivecbt_num_assets.argtypes = [c_void_p]

roivecbt_submit_buy_order = lib.roivecbt_submit_buy_order
roivecbt_submit_buy_order.restype = c_int64
roivecbt_submit_buy_order.argtypes = [
    c_void_p,
    c_uint64,
    c_int64,
    c_float,
    c_float,
    c_uint8,
    c_uint8,
    c_bool
]

roivecbt_submit_sell_order = lib.roivecbt_submit_sell_order
roivecbt_submit_sell_order.restype = c_int64
roivecbt_submit_sell_order.argtypes = [
    c_void_p,
    c_uint64,
    c_int64,
    c_float,
    c_float,
    c_uint8,
    c_uint8,
    c_bool
]

roivecbt_cancel = lib.roivecbt_cancel
roivecbt_cancel.restype = c_int64
roivecbt_cancel.argtypes = [c_void_p, c_uint64, c_int64, c_bool]

roivecbt_clear_last_trades = lib.roivecbt_clear_last_trades
roivecbt_clear_last_trades.restype = c_void_p
roivecbt_clear_last_trades.argtypes = [c_void_p, c_uint64]

roivecbt_clear_inactive_orders = lib.roivecbt_clear_inactive_orders
roivecbt_clear_inactive_orders.restype = c_void_p
roivecbt_clear_inactive_orders.argtypes = [c_void_p, c_uint64]

roivecbt_orders = lib.roivecbt_orders
roivecbt_orders.restype = c_void_p
roivecbt_orders.argtypes = [c_void_p, c_uint64]

roivecbt_state_values = lib.roivecbt_state_values
roivecbt_state_values.restype = c_void_p
roivecbt_state_values.argtypes = [c_void_p, c_uint64]

roivecbt_feed_latency = lib.roivecbt_feed_latency
roivecbt_feed_latency.restype = c_bool
roivecbt_feed_latency.argtypes = [c_void_p, c_uint64, POINTER(c_int64), POINTER(c_int64)]

roivecbt_order_latency = lib.roivecbt_order_latency
roivecbt_order_latency.restype = c_bool
roivecbt_order_latency.argtypes = [c_void_p, c_uint64, POINTER(c_int64), POINTER(c_int64), POINTER(c_int64)]


class ROIVectorMarketDepthMultiAssetMultiExchangeBacktest:
    ptr: voidptr

    def __init__(self, ptr: voidptr):
        self.ptr = ptr

    @property
    def current_timestamp(self) -> int64:
        """
        In backtesting, this timestamp reflects the time at which the backtesting is conducted within the provided data.
        """
        return roivecbt_current_timestamp(self.ptr)

    def depth_typed(self, asset_no: uint64) -> ROIVectorMarketDepth:
        """
        Args:
            asset_no: Asset number from which the market depth will be retrieved.

        Returns:
            The depth of market of the specific asset.
        """
        return ROIVectorMarketDepth_(roivecbt_depth_typed(self.ptr, asset_no))

    @property
    def num_assets(self) -> uint64:
        """
        Returns the number of assets.
        """
        return roivecbt_num_assets(self.ptr)

    def position(self, asset_no: uint64) -> float64:
        """
        Args:
            asset_no: Asset number from which the position will be retrieved.

        Returns:
            The quantity of the held position.
        """
        return roivecbt_position(self.ptr, asset_no)

    def state_values(self, asset_no: uint64) -> state_values_dtype:
        """
        Args:
            asset_no: Asset number from which the state values will be retrieved.

        Returns:
            The state’s values.
        """
        ptr = roivecbt_state_values(self.ptr, asset_no)
        return numba.carray(
            address_as_void_pointer(ptr),
            1,
            state_values_dtype
        )

    def trade_typed(self, asset_no: uint64) -> EVENT_ARRAY:
        """
        Args:
            asset_no: Asset number from which the trades will be retrieved.

        Returns:
            An array of `Event` representing trades occurring in the market for the specific asset.
        """
        length = uint64(0)
        len_ptr = ptr_from_val(length)
        ptr = roivecbt_trade_typed(self.ptr, asset_no, len_ptr)
        return numba.carray(
            address_as_void_pointer(ptr),
            val_from_ptr(len_ptr),
            event_dtype
        )

    def clear_last_trades(self, asset_no: uint64) -> None:
        """
        Clears the last trades occurring in the market from the buffer for :func:`trade_typed`.

        Args:
            asset_no: Asset number at which this command will be executed. If :const:`ALL_ASSETS`, all last trades in
                      any assets will be cleared.
        """
        roivecbt_clear_last_trades(self.ptr, asset_no)

    def orders(self, asset_no: uint64) -> OrderDict:
        """
        Args:
            asset_no: Asset number from which orders will be retrieved.

        Returns:
            An order dictionary where the keys are order IDs and the corresponding values are :class:`Order`s.
        """
        return OrderDict_(roivecbt_orders(self.ptr, asset_no))

    def submit_buy_order(
            self,
            asset_no: uint64,
            order_id: int64,
            price: float32,
            qty: float32,
            time_in_force: uint8,
            order_type: uint8,
            wait: bool
    ) -> int64:
        """
        Submits a buy order.

        Args:
            asset_no: Asset number at which this command will be executed.
            order_id: The unique order ID; there should not be any existing order with the same ID on both local and
                      exchange sides.
            price: Order price.
            qty: Quantity to buy.
            time_in_force: Available options vary depending on the exchange model. See to the exchange model for
                           details.

                * :const:`GTC`
                * :const:`GTX`
                * :const:`FOK`
                * :const:`IOC`
            order_type: Available options vary depending on the exchange model. See to the exchange model for details.

                * :const:`LIMIT`
                * :const:`MARKET`
            wait: If `True`, wait until the order placement response is received.

        Returns:
            -1 when an error occurs; otherwise, it succeeds in submitting a buy order.
        """
        return roivecbt_submit_buy_order(self.ptr, asset_no, order_id, price, qty, time_in_force, order_type, wait)

    def submit_sell_order(
            self,
            asset_no: uint64,
            order_id: int64,
            price: float32,
            qty: float32,
            time_in_force: uint8,
            order_type: uint8,
            wait: bool
    ) -> int64:
        """
        Submits a sell order.

        Args:
            asset_no: Asset number at which this command will be executed.
            order_id: The unique order ID; there should not be any existing order with the same ID on both local and
                      exchange sides.
            price: Order price.
            qty: Quantity to buy.
            time_in_force: Available options vary depending on the exchange model. See to the exchange model for
                           details.

                * :const:`GTC`
                * :const:`GTX`
                * :const:`FOK`
                * :const:`IOC`
            order_type: Available options vary depending on the exchange model. See to the exchange model for details.

                * :const:`LIMIT`
                * :const:`MARKET`
            wait: If `True`, wait until the order placement response is received.

        Returns:
            `-1` when an error occurs; otherwise, it succeeds in submitting a sell order.
        """
        return roivecbt_submit_sell_order(self.ptr, asset_no, order_id, price, qty, time_in_force, order_type, wait)

    def cancel(self, asset_no: uint64, order_id: int64, wait: bool) -> int64:
        """
        Cancels the specified order.

        Args:
            asset_no: Asset number at which this command will be executed.
            order_id: Order ID to cancel.
            wait: If `True`, wait until the order cancel response is received.

        Returns:
            `-1` when an error occurs; otherwise, it successfully submits a cancel order.
        """
        return roivecbt_cancel(self.ptr, asset_no, order_id, wait)

    def clear_inactive_orders(self, asset_no: uint64) -> None:
        """
        Clears inactive orders from the local order dictionary whose status is neither :const:`NEW` nor
        :const:`PARTIALLY_FILLED`.

        Args:
            asset_no: Asset number at which this command will be executed. If :const:`ALL_ASSETS`, all inactive orders
                      in any assets will be cleared.
        """
        roivecbt_clear_inactive_orders(self.ptr, asset_no)

    def wait_order_response(self, asset_no: uint64, order_id: int64, timeout: int64) -> int64:
        """
        Waits for the response of the order with the given order ID until timeout.

        Args:
            asset_no: Asset number where an order with `order_id` exists.
            order_id: Order ID to wait for the response.
            timeout: Timeout for waiting for the order response. Nanoseconds is the default unit. However, unit should
                     be the same as the data’s timestamp unit.

        Returns:
            * `1` when it receives an order response for the specified order ID of the specified asset number.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return roivecbt_roivecbt_wait_order_response(self.ptr, asset_no, order_id, timeout)

    def wait_next_feed(self, include_order_resp: bool, timeout: int64) -> int64:
        """
        Waits until the next feed is received, or until timeout.

        Args:
            include_order_resp: If set to `True`, it will return when any order response is received, in addition to the
                                next feed.
            timeout: Timeout for waiting for the next feed or an order response. Nanoseconds is the default unit.
                     However, unit should be the same as the data’s timestamp unit.

        Returns:
            * `1` when it receives a feed or an order response.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return roivecbt_wait_next_feed(self.ptr, include_order_resp, timeout)

    def elapse(self, duration: uint64) -> int64:
        """
        Elapses the specified duration.

        Args:
            duration: Duration to elapse. Nanoseconds is the default unit. However, unit should be the same as the
                      data’s timestamp unit.

        Returns:
            * `1` when it reaches the specified timestamp within the data.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return roivecbt_elapse(self.ptr, duration)

    def elapse_bt(self, duration: int64) -> int64:
        """
        Elapses time only in backtesting. In live mode, it is ignored. (Supported only in the Rust implementation)

        The `elapse` method exclusively manages time during backtesting, meaning that factors such as computing time are
        not properly accounted for. So, this method can be utilized to simulate such processing times.

        Args:
            duration: Duration to elapse. Nanoseconds is the default unit. However, unit should be the same as the
                      data’s timestamp unit.

        Returns:
            * `1` when it reaches the specified timestamp within the data.
            * `0` when it reaches the end of the data.
            * `-1` when an error occurs.
        """
        return roivecbt_elapse_bt(self.ptr, duration)

    def close(self) -> int64:
        """
        Closes this backtester or bot.

        Returns:
            `-1` when an error occurs; otherwise, it successfully closes the bot.
        """
        return roivecbt_close(self.ptr)

    def feed_latency(self, asset_no: uint64) -> Tuple[int64, int64] | None:
        """
        Args:
            asset_no: Asset number from which the last feed latency will be retrieved.

        Returns:
            The last feed’s exchange timestamp and local receipt timestamp if a feed has been received; otherwise,
            returns `None`.
        """
        exch_ts = int64(0)
        local_ts = int64(0)
        exch_ts_ptr = ptr_from_val(exch_ts)
        local_ts_ptr = ptr_from_val(local_ts)
        if roivecbt_feed_latency(self.ptr, asset_no, exch_ts_ptr, local_ts_ptr):
            return val_from_ptr(exch_ts_ptr), val_from_ptr(local_ts_ptr)
        return None

    def order_latency(self, asset_no: uint64) -> Tuple[int64, int64, int64] | None:
        """
        Args:
            asset_no: Asset number from which the last order latency will be retrieved.

        Returns:
            The last order’s request timestamp, exchange timestamp, and response receipt timestamp if there has been an
            order submission; otherwise, returns `None`.
        """
        req_ts = int64(0)
        exch_ts = int64(0)
        resp_ts = int64(0)
        req_ts_ptr = ptr_from_val(req_ts)
        exch_ts_ptr = ptr_from_val(exch_ts)
        resp_ts_ptr = ptr_from_val(resp_ts)
        if roivecbt_order_latency(self.ptr, asset_no, req_ts_ptr, exch_ts_ptr, resp_ts_ptr):
            return val_from_ptr(req_ts_ptr), val_from_ptr(exch_ts_ptr), val_from_ptr(resp_ts_ptr)
        return None


ROIVectorMarketDepthMultiAssetMultiExchangeBacktest_ = jitclass(ROIVectorMarketDepthMultiAssetMultiExchangeBacktest)