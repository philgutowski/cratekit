import Foundation

/// Any JSON value, for the parts of an envelope whose shape belongs to one
/// verb: its `data`, a cause's `detail`. Decoded whole, so nothing a verb
/// printed is dropped on the way to the screen.
public enum JSONValue: Equatable, Sendable {
    case null
    case bool(Bool)
    case number(Double)
    case string(String)
    case array([JSONValue])
    case object([String: JSONValue])

    /// The value under `key` when this is an object, else nil.
    public subscript(key: String) -> JSONValue? {
        if case .object(let members) = self { return members[key] }
        return nil
    }

    /// The element at `index` when this is an array and the index is in it.
    public subscript(index: Int) -> JSONValue? {
        if case .array(let elements) = self, elements.indices.contains(index) {
            return elements[index]
        }
        return nil
    }

    public var stringValue: String? {
        if case .string(let text) = self { return text }
        return nil
    }

    public var numberValue: Double? {
        if case .number(let number) = self { return number }
        return nil
    }

    public var boolValue: Bool? {
        if case .bool(let flag) = self { return flag }
        return nil
    }

    public var arrayValue: [JSONValue]? {
        if case .array(let elements) = self { return elements }
        return nil
    }

    public var objectValue: [String: JSONValue]? {
        if case .object(let members) = self { return members }
        return nil
    }

    public var isNull: Bool { self == .null }
}

extension JSONValue: Decodable {
    public init(from decoder: Decoder) throws {
        let container = try decoder.singleValueContainer()
        if container.decodeNil() {
            self = .null
        } else if let flag = try? container.decode(Bool.self) {
            // Before numbers, so true and false never read as 1 and 0.
            self = .bool(flag)
        } else if let number = try? container.decode(Double.self) {
            self = .number(number)
        } else if let text = try? container.decode(String.self) {
            self = .string(text)
        } else if let elements = try? container.decode([JSONValue].self) {
            self = .array(elements)
        } else if let members = try? container.decode([String: JSONValue].self) {
            self = .object(members)
        } else {
            throw DecodingError.dataCorruptedError(
                in: container, debugDescription: "a value that is not JSON")
        }
    }
}
